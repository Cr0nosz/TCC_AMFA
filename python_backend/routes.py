from flask import Blueprint, request, session, jsonify
from datetime import datetime, timedelta
import bcrypt
from models import db, User, AccessLog, SecuritySession, LoginAttempt, get_sp_now
from email_service import (
    generate_verification_code, hash_verification_code,
    send_verification_code_email, send_security_alert_email
)
from security import (
    get_location_from_ip, extract_device_info, get_client_ip,
    check_brute_force, check_impossible_travel, check_location_proximity
)
from config import Config

auth_bp = Blueprint('auth', __name__)

# Criptografia do Hash para evitar ataques
DUMMY_BCRYPT_HASH = b'$2b$12$C6UzMDM.H6dfI/f/IKcEe.8U1i1r7rGfKQzWvYb1g4E9aW1u6bD7e'

# Exige a autenticação
def require_auth():
    if 'userId' not in session:
        return jsonify({'message': 'Autenticação necessária'}), 401
    return None

# POST /api/auth/register
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email', '').lower().strip()
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400
    
    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Usuário já existe com este email'}), 409
    
    # Senha Hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(Config.BCRYPT_LOG_ROUNDS))
    
    # Cria usuário
    user = User(
        name=name,
        email=email,
        password=hashed_password.decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    
    # Pega informações do cliente
    client_ip = get_client_ip(request)
    location = get_location_from_ip(client_ip)
    device_info = extract_device_info(request.headers.get('User-Agent', ''))
    
    # Registração de informações em log
    access_log = AccessLog(
        user_id=user.id,
        action='register',
        success=True,
        ip_address=client_ip,
        user_agent=request.headers.get('User-Agent'),
        location=location,
        device_info=device_info
    )
    db.session.add(access_log)
    db.session.commit()
    
    # Gera e envia códigos de verificação
    try:
        code, expires_at = generate_verification_code()
        code_hash = hash_verification_code(code)
        
        user.email_verification_code_hash = code_hash
        user.email_verification_expires_at = expires_at
        user.last_email_verification_sent_at = get_sp_now()
        db.session.commit()
        
        send_verification_code_email(email, name, code)
        print(f'Verification code sent to {email}')
    except Exception as e:
        print(f'Falha ao enviar email de verificação: {e}')
    
    return jsonify({
        'message': 'Usuário registrado com sucesso. Verifique seu email para obter o código de verificação.',
        'requiresEmailVerification': True
    }), 201

# POST /api/auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').lower().strip()
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400
    
    client_ip = get_client_ip(request)
    
    # Checa se for ataque de brute_force
    brute_force_check = check_brute_force(email, client_ip, db)
    if brute_force_check['isBlocked']:
        return jsonify({
            'message': brute_force_check['reason'],
            'error': 'SECURITY_BLOCKED',
            'blockedUntil': brute_force_check['blockedUntil'].isoformat() if brute_force_check.get('blockedUntil') else None
        }), 429
    
    # Busca o usuário
    user = User.query.filter_by(email=email).first()
    
    # Verifica senha (ou verificações falsas para prenvenção de ataques)
    is_valid_password = False
    if user:
        is_valid_password = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    else:
        bcrypt.checkpw(password.encode('utf-8'), DUMMY_BCRYPT_HASH)
    
    # Checa todas as condições
    if not user or not is_valid_password or not user.is_email_confirmed:
        # Registra falha de login
        login_attempt = LoginAttempt(
            email=email,
            ip_address=client_ip,
            success=False
        )
        db.session.add(login_attempt)
        
        location = get_location_from_ip(client_ip)
        device_info = extract_device_info(request.headers.get('User-Agent', ''))
        
        access_log = AccessLog(
            user_id=user.id if user else None,
            action='login',
            success=False,
            ip_address=client_ip,
            user_agent=request.headers.get('User-Agent'),
            location=location,
            device_info=device_info
        )
        db.session.add(access_log)
        db.session.commit()
        
        return jsonify({
            'message': 'Credenciais inválidas ou conta não verificada. Verifique seu email e senha.'
        }), 401
    
    # Busca a localização para confirmar usuário
    current_location = get_location_from_ip(client_ip)
    
    # Verifica se viagem impossivel
    if current_location and current_location.get('lat') and current_location.get('lng'):
        impossible_travel = check_impossible_travel(user.id, current_location, db)
        if impossible_travel['isImpossible']:
            # Cria sessão de segurança
            code, expires_at = generate_verification_code()
            code_hash = hash_verification_code(code)
            
            sec_session = SecuritySession(
                user_id=user.id,
                ip_address=client_ip,
                user_agent=request.headers.get('User-Agent'),
                location=current_location,
                device_info=extract_device_info(request.headers.get('User-Agent', '')),
                security_code_hash=code_hash,
                expires_at=expires_at
            )
            db.session.add(sec_session)
            db.session.commit()
            
            # Envia email de alerta 
            try:
                send_security_alert_email(user.email, user.name, code, client_ip, current_location)
            except Exception as e:
                print(f'Falha ao enviar email de alerta de segurança: {e}')
            
            return jsonify({
                'requiresSecurity': True,
                'sessionId': sec_session.id,
                'userEmail': user.email,
                'message': 'Detectamos acesso de localização desconhecida. Verifique seu email.'
            }), 200
    
    # Checa se o ip é conhecido
    ip_known = AccessLog.query.filter_by(
        user_id=user.id,
        ip_address=client_ip,
        success=True
    ).first() is not None
    
    # Verifica se localização é próxima
    if current_location and current_location.get('lat') and current_location.get('lng') and not ip_known:
        proximity = check_location_proximity(user.id, current_location, db)
        if not proximity['isNearby']:
            # Criar sessão de segurança
            code, expires_at = generate_verification_code()
            code_hash = hash_verification_code(code)
            
            sec_session = SecuritySession(
                user_id=user.id,
                ip_address=client_ip,
                user_agent=request.headers.get('User-Agent'),
                location=current_location,
                device_info=extract_device_info(request.headers.get('User-Agent', '')),
                security_code_hash=code_hash,
                expires_at=expires_at
            )
            db.session.add(sec_session)
            db.session.commit()
            
            # Enviar e-mail de alerta de segurança
            try:
                send_security_alert_email(user.email, user.name, code, client_ip, current_location)
            except Exception as e:
                print(f'Falha ao enviar email de alerta de segurança: {e}')
            
            return jsonify({
                'requiresSecurity': True,
                'sessionId': sec_session.id,
                'userEmail': user.email,
                'message': 'Detectamos acesso de localização desconhecida. Verifique seu email.'
            }), 200
    
    # Login bem-sucedido
    login_attempt = LoginAttempt(
        email=email,
        ip_address=client_ip,
        success=True
    )
    db.session.add(login_attempt)
    
    location = get_location_from_ip(client_ip)
    device_info = extract_device_info(request.headers.get('User-Agent', ''))
    
    access_log = AccessLog(
        user_id=user.id,
        action='login',
        success=True,
        ip_address=client_ip,
        user_agent=request.headers.get('User-Agent'),
        location=location,
        device_info=device_info
    )
    db.session.add(access_log)
    db.session.commit()
    
    # Definir sessão
    session['userId'] = user.id
    session['userRole'] = user.role
    
    return jsonify({'message': 'Login realizado com sucesso', 'user': user.to_dict()}), 200

# POST /api/auth/verify-code - Verificação de e-mail
@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    email = data.get('email', '').lower().strip()
    code = data.get('code')
    
    if not email or not code:
        return jsonify({'message': 'Email e código são obrigatórios'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Verificar se o código existe
    if not user.email_verification_code_hash:
        return jsonify({'message': 'Nenhum código de verificação encontrado'}), 400
    
    # Verificar se o código expirou
    if user.email_verification_expires_at and get_sp_now() > user.email_verification_expires_at:
        return jsonify({'message': 'Código de verificação expirado'}), 400
    
    # Verificar código
    code_hash = hash_verification_code(code)
    if code_hash != user.email_verification_code_hash:
        user.email_verification_attempts += 1
        user.last_verification_attempt_at = get_sp_now()
        db.session.commit()
        return jsonify({'message': 'Código de verificação inválido'}), 400
    
    # Marcar e-mail como confirmado
    user.is_email_confirmed = True
    user.email_verification_code_hash = None
    user.email_verification_expires_at = None
    user.email_verification_attempts = 0
    db.session.commit()
    
    # Criar sessão
    session['userId'] = user.id
    session['userRole'] = user.role
    
    return jsonify({'message': 'Email verificado com sucesso', 'user': user.to_dict()}), 200

# POST /api/auth/resend-verification-code
@auth_bp.route('/resend-verification-code', methods=['POST'])
def resend_verification_code():
    data = request.json
    email = data.get('email', '').lower().strip()
    
    if not email:
        return jsonify({'message': 'Email é obrigatório'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Verificar se já está confirmado
    if user.is_email_confirmed:
        return jsonify({'message': 'Email já está verificado'}), 400
    
    # Limitação de taxa: máximo de 1 e-mail por minuto
    if user.last_email_verification_sent_at:
        time_since_last = (get_sp_now() - user.last_email_verification_sent_at).total_seconds()
        if time_since_last < 60:
            return jsonify({'message': f'Aguarde {60 - int(time_since_last)} segundos antes de solicitar um novo código'}), 429
    
    # Gerar novo código
    code, expires_at = generate_verification_code()
    code_hash = hash_verification_code(code)
    
    user.email_verification_code_hash = code_hash
    user.email_verification_expires_at = expires_at
    user.last_email_verification_sent_at = get_sp_now()
    db.session.commit()
    
    # Enviar e-mail
    try:
        send_verification_code_email(user.email, user.name, code)
        return jsonify({'message': 'Novo código de verificação enviado'}), 200
    except Exception as e:
        print(f'Falha ao enviar email de verificação: {e}')
        return jsonify({'message': 'Erro ao enviar email de verificação'}), 500

# POST /api/auth/verify-security
@auth_bp.route('/verify-security', methods=['POST'])
def verify_security():
    data = request.json
    session_id = data.get('sessionId')
    code = data.get('code')
    
    if not session_id or not code:
        return jsonify({'message': 'SessionId e código são obrigatórios'}), 400
    
    sec_session = SecuritySession.query.get(session_id)
    if not sec_session:
        return jsonify({'message': 'Sessão de segurança não encontrada'}), 404
    
    # Verificar se expirou
    if get_sp_now() > sec_session.expires_at:
        return jsonify({'message': 'Sessão de segurança expirada'}), 400
    
    # Verificar tentativas
    if sec_session.verification_attempts >= sec_session.max_attempts:
        return jsonify({'message': 'Número máximo de tentativas excedido'}), 400
    
    # Verificar código
    code_hash = hash_verification_code(code)
    if code_hash != sec_session.security_code_hash:
        sec_session.verification_attempts += 1
        db.session.commit()
        return jsonify({'message': 'Código de segurança inválido'}), 400
    
    # Marcar como confirmado
    sec_session.is_confirmed = True
    db.session.commit()
    
    # Criar sessão de usuário
    user = User.query.get(sec_session.user_id)
    session['userId'] = user.id
    session['userRole'] = user.role
    
    # Registrar login bem-sucedido
    access_log = AccessLog(
        user_id=user.id,
        action='login',
        success=True,
        ip_address=sec_session.ip_address,
        user_agent=sec_session.user_agent,
        location=sec_session.location,
        device_info=sec_session.device_info
    )
    db.session.add(access_log)
    db.session.commit()
    
    return jsonify({'message': 'Verificação de segurança aprovada', 'user': user.to_dict()}), 200

# POST /api/auth/resend-security-code
@auth_bp.route('/resend-security-code', methods=['POST'])
def resend_security_code():
    data = request.json
    session_id = data.get('sessionId')
    
    if not session_id:
        return jsonify({'message': 'SessionId é obrigatório'}), 400
    
    sec_session = SecuritySession.query.get(session_id)
    if not sec_session:
        return jsonify({'message': 'Sessão de segurança não encontrada'}), 404
    
    # Gerar novo código
    code, expires_at = generate_verification_code()
    code_hash = hash_verification_code(code)
    
    sec_session.security_code_hash = code_hash
    sec_session.expires_at = expires_at
    sec_session.verification_attempts = 0
    db.session.commit()
    
    # Enviar e-mail
    user = User.query.get(sec_session.user_id)
    try:
        send_security_alert_email(user.email, user.name, code, sec_session.ip_address, sec_session.location)
        return jsonify({'message': 'Novo código de segurança enviado'}), 200
    except Exception as e:
        print(f'Falha ao enviar email de alerta de segurança: {e}')
        return jsonify({'message': 'Erro ao enviar email de segurança'}), 500

# GET /api/auth/me
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(session['userId'])
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200

# GET /api/auth/access-logs
@auth_bp.route('/access-logs', methods=['GET'])
def get_access_logs():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    logs = AccessLog.query.filter_by(user_id=session['userId']).order_by(AccessLog.login_time.desc()).limit(50).all()
    return jsonify({'logs': [log.to_dict() for log in logs]}), 200

# POST /api/auth/logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user_id = session['userId']
    
    # Registrar logout
    client_ip = get_client_ip(request)
    location = get_location_from_ip(client_ip)
    device_info = extract_device_info(request.headers.get('User-Agent', ''))
    
    access_log = AccessLog(
        user_id=user_id,
        action='logout',
        success=True,
        ip_address=client_ip,
        user_agent=request.headers.get('User-Agent'),
        location=location,
        device_info=device_info
    )
    db.session.add(access_log)
    db.session.commit()
    
    # Limpar sessão
    session.clear()
    
    return jsonify({'message': 'Logout realizado com sucesso'}), 200