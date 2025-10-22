import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (sem sobrescrever as já existentes)
load_dotenv(override=False)

class Config:
 
    # BANCO DE DADOS
 
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Se não encontrar, tenta recarregar o .env sobrescrevendo variáveis
    if not DATABASE_URL:
        load_dotenv(override=True)
        DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Interrompe se o banco não estiver configurado
    if not DATABASE_URL:
        raise ValueError("A variável DATABASE_URL é obrigatória")
    
 
    # SESSÃO
   
    SECRET_KEY = os.getenv('SESSION_SECRET', 'your-super-secret-session-key-change-in-production')
    SESSION_TYPE = 'sqlalchemy'              # Armazena sessões no banco
    SESSION_PERMANENT = False                # Sessão expira ao fechar o navegador
    SESSION_USE_SIGNER = True                # Assina cookies para evitar alterações
    SESSION_COOKIE_NAME = 'amfa.sid'         # Nome do cookie da sessão
    SESSION_COOKIE_HTTPONLY = True           # Impede acesso via JavaScript
    SESSION_COOKIE_SECURE = os.getenv('NODE_ENV') == 'production'  # HTTPS apenas em produção
    SESSION_COOKIE_SAMESITE = 'Lax'          # Restringe envio de cookies entre sites
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # Duração máxima: 24 horas
    
  
    # E-MAIL
   
    SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM = os.getenv('SMTP_FROM', 'noreply@localhost')
    SMTP_SECURE = os.getenv('SMTP_PORT') == '465'  # Usa SSL se a porta for 465
    

    # APLICAÇÃO
    
    APP_URL = os.getenv('APP_URL', 'http://localhost:5000')  # URL base da aplicação
    
  
    # SEGURANÇA

    BCRYPT_LOG_ROUNDS = 12                     # Nível de força do hash de senha
    VERIFICATION_CODE_EXPIRY_MINUTES = 15      # Expiração do código de verificação
    SECURITY_CODE_EXPIRY_MINUTES = 30          # Expiração do código MFA
    MAX_LOGIN_ATTEMPTS_PER_EMAIL = 5           # Tentativas máximas por e-mail
    MAX_LOGIN_ATTEMPTS_PER_IP = 10             # Tentativas máximas por IP
    BRUTE_FORCE_WINDOW_MINUTES = 2             # Janela de contagem de tentativas
    EMAIL_BLOCK_MINUTES = 15                   # Tempo de bloqueio por e-mail
    IP_BLOCK_MINUTES = 30                      # Tempo de bloqueio por IP
