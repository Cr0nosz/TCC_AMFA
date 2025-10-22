import requests
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from models import get_sp_now

# Cache para mapeamentos de IP para localização (TTL de 24 horas)
location_cache = {}
LOCATION_CACHE_TTL = 24 * 60 * 60  # 24 horas em segundos

def is_private_ip(ip):
    """Verifica se o IP é privado/local"""
    # Remove o prefixo IPv4 mapeado para IPv6
    normalized_ip = ip.replace('::ffff:', '')
    
    # Verifica endereços locais/loopback
    if normalized_ip in ['::1', 'unknown'] or normalized_ip.startswith('127.'):
        return True
    
    # Verifica faixas de IP privadas IPv4
    parts = normalized_ip.split('.')
    if len(parts) == 4:
        try:
            octets = [int(p) for p in parts]
            
            # 10.0.0.0/8
            if octets[0] == 10:
                return True
            
            # 172.16.0.0/12
            if octets[0] == 172 and 16 <= octets[1] <= 31:
                return True
            
            # 192.168.0.0/16
            if octets[0] == 192 and octets[1] == 168:
                return True
        except ValueError:
            pass
    
    # Verifica faixas de IP privadas IPv6
    if normalized_ip.startswith(('fc00:', 'fd00:', 'fe80:')):
        return True
    
    return False

def get_location_from_ip(ip_address):
    """Obtém informações de localização a partir do endereço IP"""
    if is_private_ip(ip_address):
        return None
    
    # Verifica o cache
    now = get_sp_now().timestamp()
    if ip_address in location_cache:
        cached = location_cache[ip_address]
        if (now - cached['timestamp']) < LOCATION_CACHE_TTL:
            return cached['location']
    
    try:
        response = requests.get(
            f'https://ipapi.co/{ip_address}/json/',
            headers={'User-Agent': 'Mozilla/5.0 (compatible; Location-Tracker/1.0)'},
            timeout=2
        )
        
        if response.status_code != 200:
            print(f'Falha na busca de localização para IP {ip_address}: {response.status_code}')
            return None
        
        data = response.json()
        
        if data.get('error') or not data.get('city') or not data.get('region') or not data.get('country_name'):
            print(f'Dados de localização inválidos para IP {ip_address}')
            return None
        
        location = {
            'city': data['city'],
            'region': data['region'],
            'country': data['country_name'],
            'lat': data.get('latitude'),
            'lng': data.get('longitude')
        }
        
        # Armazena o resultado em cache
        location_cache[ip_address] = {
            'location': location,
            'timestamp': now
        }
        
        return location
    except Exception as e:
        print(f'Erro ao obter localização para IP {ip_address}: {e}')
        return None

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine"""
    R = 6371  # Raio da Terra em quilômetros
    
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

def check_impossible_travel(user_id, current_location, db):
    """Verifica viagens impossíveis com base em logs de acesso recentes"""
    from models import AccessLog
    
    if not current_location or not current_location.get('lat') or not current_location.get('lng'):
        return {'isImpossible': False}
    
    # Obtém logs de acesso recentes (últimas 48 horas)
    forty_eight_hours_ago = get_sp_now() - timedelta(hours=48)
    recent_logs = AccessLog.query.filter(
        AccessLog.user_id == user_id,
        AccessLog.login_time >= forty_eight_hours_ago,
        AccessLog.location.isnot(None)
    ).order_by(AccessLog.login_time.desc()).all()
    
    for log in recent_logs:
        if log.location and log.location.get('lat') and log.location.get('lng'):
            distance = calculate_distance(
                log.location['lat'],
                log.location['lng'],
                current_location['lat'],
                current_location['lng']
            )
            
            time_diff = (get_sp_now() - log.login_time).total_seconds() / 3600  # horas
            
            IMPOSSIBLE_DISTANCE_KM = 500
            MIN_TIME_HOURS = 2
            
            if distance > IMPOSSIBLE_DISTANCE_KM and time_diff < MIN_TIME_HOURS:
                print(f'Impossible travel detected for user {user_id}: {distance:.2f}km in {time_diff:.2f} hours')
                return {
                    'isImpossible': True,
                    'distance': round(distance),
                    'timeDiff': round(time_diff, 2)
                }
    
    return {'isImpossible': False}

def check_location_proximity(user_id, current_location, db):
    """Verifica se a nova localização IP está próxima (verificação de proximidade)"""
    from models import AccessLog
    
    if not current_location or not current_location.get('lat') or not current_location.get('lng'):
        return {'isNearby': False}
    
    # Obtém logs de acesso bem-sucedidos recentes (últimos 30 dias)
    thirty_days_ago = get_sp_now() - timedelta(days=30)
    recent_logs = AccessLog.query.filter(
        AccessLog.user_id == user_id,
        AccessLog.login_time >= thirty_days_ago,
        AccessLog.success == True,
        AccessLog.location.isnot(None)
    ).order_by(AccessLog.login_time.desc()).all()
    
    for log in recent_logs:
        if log.location and log.location.get('lat') and log.location.get('lng'):
            distance = calculate_distance(
                log.location['lat'],
                log.location['lng'],
                current_location['lat'],
                current_location['lng']
            )
            
            PROXIMITY_DISTANCE_KM = 100
            is_nearby = distance <= PROXIMITY_DISTANCE_KM
            
            print(f'Location proximity check for user {user_id}: {distance:.2f}km from last known location (nearby: {is_nearby})')
            
            return {
                'isNearby': is_nearby,
                'distance': round(distance)
            }
    
    return {'isNearby': False}

def check_brute_force(email, ip_address, db):
    """Detecta ataques de força bruta"""
    from models import LoginAttempt, SecurityBlock
    
    now = get_sp_now()
    two_minutes_ago = now - timedelta(minutes=2)
    
    # Verifica tentativas falhas recentes por e-mail
    recent_email_attempts = LoginAttempt.query.filter(
        LoginAttempt.email == email,
        LoginAttempt.attempted_at >= two_minutes_ago,
        LoginAttempt.success == False
    ).count()
    
    # Verifica tentativas falhas recentes por IP
    recent_ip_attempts = LoginAttempt.query.filter(
        LoginAttempt.ip_address == ip_address,
        LoginAttempt.attempted_at >= two_minutes_ago,
        LoginAttempt.success == False
    ).count()
    
    # Verifica bloqueios ativos
    active_blocks = SecurityBlock.query.filter(
        db.or_(
            SecurityBlock.email == email,
            SecurityBlock.ip_address == ip_address
        ),
        SecurityBlock.is_active == True,
        db.or_(
            SecurityBlock.blocked_until.is_(None),
            SecurityBlock.blocked_until > now
        )
    ).first()
    
    if active_blocks:
        if active_blocks.blocked_until and now < active_blocks.blocked_until:
            return {
                'isBlocked': True,
                'reason': f'Blocked due to {active_blocks.block_reason}',
                'blockedUntil': active_blocks.blocked_until
            }
    
    MAX_ATTEMPTS_PER_EMAIL = 5
    MAX_ATTEMPTS_PER_IP = 10
    
    if recent_email_attempts >= MAX_ATTEMPTS_PER_EMAIL:
        blocked_until = now + timedelta(minutes=15)
        block = SecurityBlock(
            email=email,
            ip_address=ip_address,
            block_reason='brute_force',
            blocked_until=blocked_until,
            is_active=True
        )
        db.session.add(block)
        db.session.commit()
        
        print(f'Email {email} blocked for brute force until {blocked_until}')
        return {
            'isBlocked': True,
            'reason': 'Muitas tentativas de login falharam para este email',
            'blockedUntil': blocked_until
        }
    
    if recent_ip_attempts >= MAX_ATTEMPTS_PER_IP:
        blocked_until = now + timedelta(minutes=30)
        block = SecurityBlock(
            email=email,
            ip_address=ip_address,
            block_reason='brute_force',
            blocked_until=blocked_until,
            is_active=True
        )
        db.session.add(block)
        db.session.commit()
        
        print(f'IP {ip_address} blocked for brute force until {blocked_until}')
        return {
            'isBlocked': True,
            'reason': 'Muitas tentativas de login falharam a partir deste endereço IP',
            'blockedUntil': blocked_until
        }
    
    return {'isBlocked': False}

def extract_device_info(user_agent):
    """Extrai informações do dispositivo da string user-agent"""
    if not user_agent:
        return {'browser': 'Unknown', 'os': 'Unknown'}
    
    browser = 'Unknown'
    os = 'Unknown'
    
    # Detecta navegador
    if 'Chrome' in user_agent:
        browser = 'Chrome'
    elif 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Safari' in user_agent:
        browser = 'Safari'
    elif 'Edge' in user_agent:
        browser = 'Edge'
    elif 'Opera' in user_agent:
        browser = 'Opera'
    
    # Detecta SO
    if 'Windows' in user_agent:
        os = 'Windows'
    elif 'Mac' in user_agent:
        os = 'Mac'
    elif 'Linux' in user_agent:
        os = 'Linux'
    elif 'Android' in user_agent:
        os = 'Android'
    elif 'iOS' in user_agent:
        os = 'iOS'
    
    return {'browser': browser, 'os': os}

def get_client_ip(request):
    """Obtém o endereço IP do cliente a partir da requisição"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or 'unknown'
