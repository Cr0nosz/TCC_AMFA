import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import hashlib
from datetime import datetime, timedelta
from config import Config
from models import get_sp_now

# função que checa se o email está configurado

def is_email_configured():
    return bool(Config.SMTP_HOST and Config.SMTP_USER and Config.SMTP_PASSWORD and Config.SMTP_FROM)


# Gera um código de verificação de 6 digitos 

def generate_verification_code():
    code = str(secrets.randbelow(1000000)).zfill(6)
    expires_at = get_sp_now() + timedelta(minutes=Config.VERIFICATION_CODE_EXPIRY_MINUTES)
    return code, expires_at

# código de verificação Hash 

def hash_verification_code(code):
    return hashlib.sha256(code.encode()).hexdigest()

# Envia o código de verificação pelo email

def send_verification_code_email(email, name, code):
    if not is_email_configured():
        print('Email não configurado, pulando envio de email de verificação')
        return
    
    subject = 'Código de verificação - AMFA'
    
    html_body = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
            body {{ font-family: 'JetBrains Mono', monospace; line-height: 1.6; color: hsl(180, 5%, 90%); background: hsl(180, 15%, 8%); margin: 0; padding: 20px; min-height: 100vh; }}
            .container {{ max-width: 600px; margin: 0 auto; background: hsl(180, 12%, 10%); border: 1px solid hsl(180, 10%, 18%); border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px hsla(180, 15%, 0%, 0.45); }}
            .header {{ background: linear-gradient(135deg, hsl(180, 15%, 8%) 0%, hsl(180, 12%, 12%) 100%); color: hsl(200, 60%, 55%); text-align: center; padding: 40px 30px; border-bottom: 1px solid hsl(160, 80%, 45%); }}
            .logo {{ font-size: 2.5em; font-weight: 700; margin-bottom: 10px; text-shadow: 0 0 20px hsl(160, 80%, 45%); }}
            .content {{ background: hsl(180, 12%, 10%); padding: 40px 30px; color: hsl(180, 5%, 90%); }}
            .greeting {{ font-size: 1.3em; color: hsl(160, 80%, 45%); margin-bottom: 20px; font-weight: 600; }}
            .code-container {{ text-align: center; margin: 30px 0; padding: 30px; background: hsl(180, 8%, 16%); border: 2px solid hsl(160, 80%, 45%); border-radius: 12px; }}
            .verification-code {{ font-size: 3em; font-weight: 700; color: hsl(160, 80%, 45%); letter-spacing: 8px; margin: 15px 0; text-shadow: 0 0 20px hsl(160, 80%, 45%); }}
            .warning {{ background: linear-gradient(135deg, hsl(45, 100%, 8%) 0%, hsl(45, 100%, 12%) 100%); border: 1px solid hsl(45, 100%, 25%); color: hsl(45, 100%, 70%); padding: 20px; border-radius: 8px; margin: 25px 0; }}
            .footer {{ background: hsl(180, 12%, 8%); padding: 25px 30px; text-align: center; font-size: 0.8em; color: hsl(180, 5%, 65%); border-top: 1px solid hsl(180, 10%, 15%); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🔐 AMFA</div>
                <div>CÓDIGO DE VERIFICAÇÃO</div>
            </div>
            <div class="content">
                <div class="greeting">Olá, {name}!</div>
                <div>Aqui está seu código de verificação para confirmar seu email e ativar sua conta:</div>
                <div class="code-container">
                    <div>Seu código de verificação:</div>
                    <div class="verification-code">{code}</div>
                </div>
                <div>Digite este código na página de verificação para completar seu cadastro.</div>
                <div class="warning">
                    <div><strong>Importante:</strong></div>
                    Este código expira em 15 minutos por motivos de segurança.
                </div>
                <div>Se você não criou uma conta em nossa plataforma, pode ignorar este email com segurança.</div>
            </div>
            <div class="footer">
                <p>Este email foi enviado automaticamente pelo sistema AMFA.</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    send_email(email, subject, html_body)

# Envia um email de alerta

def send_security_alert_email(email, name, security_code, ip_address, location):
    if not is_email_configured():
        print('Email não configurado, pulando envio de email de alerta')
        return
    
    location_text = f"{location['city']}, {location['region']}, {location['country']}" if location else 'Localização desconhecida'
    
    subject = '🚨 Alerta de Segurança - Acesso de localização desconhecida detectado'
    
    html_body = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
            body {{ font-family: 'JetBrains Mono', monospace; line-height: 1.6; color: hsl(180, 5%, 90%); background: hsl(180, 15%, 8%); margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: hsl(180, 12%, 10%); border: 1px solid hsl(0, 80%, 45%); border-radius: 8px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, hsl(0, 80%, 15%) 0%, hsl(0, 70%, 20%) 100%); color: hsl(0, 80%, 70%); text-align: center; padding: 40px 30px; border-bottom: 1px solid hsl(0, 80%, 45%); }}
            .logo {{ font-size: 2.5em; font-weight: 700; margin-bottom: 10px; text-shadow: 0 0 20px hsl(0, 80%, 45%); }}
            .content {{ background: hsl(180, 12%, 10%); padding: 40px 30px; color: hsl(180, 5%, 90%); }}
            .security-code {{ background: linear-gradient(135deg, hsl(160, 80%, 15%) 0%, hsl(160, 70%, 20%) 100%); border: 2px solid hsl(160, 80%, 45%); border-radius: 8px; text-align: center; padding: 25px; margin: 25px 0; }}
            .code {{ font-size: 2.5em; font-weight: 700; color: hsl(160, 80%, 70%); letter-spacing: 8px; text-shadow: 0 0 10px hsl(160, 80%, 45%); }}
            .location-info {{ background: hsl(180, 12%, 12%); border: 1px solid hsl(180, 10%, 18%); border-radius: 6px; padding: 15px; margin: 15px 0; }}
            .warning {{ background: hsl(45, 80%, 15%); border: 1px solid hsl(45, 80%, 45%); color: hsl(45, 80%, 70%); padding: 20px; border-radius: 6px; margin: 20px 0; }}
            .footer {{ background: hsl(180, 12%, 8%); padding: 30px; text-align: center; font-size: 0.85em; color: hsl(180, 5%, 60%); border-top: 1px solid hsl(180, 10%, 18%); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚨 ALERTA DE SEGURANÇA</div>
                <p>AMFA</p>
            </div>
            <div class="content">
                <h2>Olá, {name}!</h2>
                <p>Detectamos uma tentativa de login em sua conta a partir de um IP/localização que não reconhecemos.</p>
                <h3>📍 Detalhes do acesso:</h3>
                <div class="location-info">
                    <strong>IP:</strong> {ip_address}<br>
                    <strong>Localização:</strong> {location_text}<br>
                    <strong>Data/Hora:</strong> {get_sp_now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
                <p><strong>Se foi você que tentou fazer login:</strong></p>
                <p>Use o código de segurança abaixo para confirmar que este acesso é legítimo:</p>
                <div class="security-code">
                    <div>CÓDIGO DE VERIFICAÇÃO DE SEGURANÇA</div>
                    <div class="code">{security_code}</div>
                    <div>⏰ Este código expira em 30 minutos</div>
                </div>
                <div class="warning">
                    <strong>🔐 Se NÃO foi você:</strong><br>
                    Sua conta pode estar sendo alvo de acesso não autorizado. Entre em contato conosco imediatamente.
                </div>
            </div>
            <div class="footer">
                <p>Este email foi enviado automaticamente pelo sistema de segurança.</p>
                <p><strong>AMFA</strong> - Protegendo seus dados 24/7
            </div>
        </div>
    </body>
    </html>
    '''
    
    send_email(email, subject, html_body)

# Envia email alertando que o usuário foi bloqueado

def send_security_block_email(email, name, block_reason, blocked_until, ip_address, location):
    if not is_email_configured():
        print('Email não configurado, pulando envio de email de bloqueio')
        return
    
    location_text = f"{location['city']}, {location['region']}, {location['country']}" if location else 'Localização desconhecida'
    reason_text = 'Tentativas excessivas de login' if block_reason == 'brute_force' else 'Viagem impossível detectada'
    
    subject = '🔒 Conta Bloqueada Temporariamente - Atividade Suspeita Detectada'
    
    html_body = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
            body {{ font-family: 'JetBrains Mono', monospace; line-height: 1.6; color: hsl(180, 5%, 90%); background: hsl(180, 15%, 8%); margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: hsl(180, 12%, 10%); border: 1px solid hsl(0, 80%, 45%); border-radius: 8px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, hsl(0, 80%, 15%) 0%, hsl(0, 70%, 20%) 100%); color: hsl(0, 80%, 70%); text-align: center; padding: 40px 30px; }}
            .content {{ padding: 40px 30px; }}
            .alert-box {{ background: hsl(0, 80%, 15%); border: 1px solid hsl(0, 80%, 45%); border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
            .footer {{ background: hsl(180, 12%, 8%); padding: 30px; text-align: center; font-size: 0.85em; color: hsl(180, 5%, 60%); border-top: 1px solid hsl(180, 10%, 18%); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 CONTA BLOQUEADA</h1>
                <p>Cyber Security Platform</p>
            </div>
            <div class="content">
                <h2>Olá, {name}!</h2>
                <div class="alert-box">
                    <h3>⚠️ Atividade Suspeita Detectada</h3>
                    <p>Sua conta foi temporariamente bloqueada por motivos de segurança.</p>
                </div>
                <p><strong>Motivo:</strong> {reason_text}</p>
                <p><strong>IP:</strong> {ip_address}</p>
                <p><strong>Localização:</strong> {location_text}</p>
                <p><strong>Bloqueado até:</strong> {blocked_until.strftime('%d/%m/%Y %H:%M:%S')}</p>
                <p>Se você não reconhece esta atividade, entre em contato conosco imediatamente.</p>
            </div>
            <div class="footer">
                <p><strong>AMFA</strong> - Protegendo seus dados 24/7
            </div>
        </div>
    </body>
    </html>
    '''
    
    send_email(email, subject, html_body)

# Função de enviar email genérico

def send_email(to_email, subject, html_body):
    if not is_email_configured():
        print(f'Email não configurado, enviaria para {to_email}: {subject}')
        return
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"Cyber Security Platform <{Config.SMTP_FROM}>"
        msg['To'] = to_email
        
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        if Config.SMTP_SECURE:
            server = smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT)
        else:
            server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
            server.starttls()
        
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f'Email sent to {to_email}: {subject}')
    except Exception as e:
        print(f'Failed to send email: {e}')
        raise
