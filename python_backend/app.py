from flask import Flask, send_from_directory, session as flask_session
from flask_cors import CORS
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from config import Config
from models import db
from routes import auth_bp

# Cria a aplicação Flask e define a pasta de arquivos estáticos (frontend)
app = Flask(__name__, static_folder='../frontend', static_url_path='/static')
app.config.from_object(Config)


# Configuração do banco de dados

app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Testa conexão antes de usar
    'pool_recycle': 300,    # Renova conexões a cada 5 min
    'pool_size': 10,
    'max_overflow': 20
}
db.init_app(app)


# Configuração da sessão

# Define como as sessões serão armazenadas e gerenciadas
app.config['SESSION_SQLALCHEMY'] = db
Session(app)


# Configuração de CORS

# Permite que o frontend acesse a API de outro domínio/origem
CORS(app, supports_credentials=True)


# Limite de requisições (Rate Limiting)

# Evita abusos e ataques de força bruta limitando o número de requisições
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"],
    storage_uri="memory://"
)


# Inicialização do banco

# Cria as tabelas se ainda não existirem
with app.app_context():
    db.create_all()
    print("Tabelas do banco criadas com sucesso")


# Registro das rotas (blueprints)

# Conecta o módulo de autenticação (auth_bp) à aplicação principal
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Função principal para servir o frontend

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serve o frontend (SPA) e arquivos estáticos.
    Se a rota for da API, retorna 404.
    Se for um arquivo existente, serve diretamente.
    Caso contrário, retorna o index.html.
    """
    # Ignora rotas da API
    if path.startswith('api/'):
        return '', 404
    
    # Se o arquivo existir, serve diretamente
    file_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    
    # Caso contrário, retorna o index.html (SPA)
    return send_from_directory(app.static_folder, 'index.html')

# Execução da aplicação

# Inicia o servidor Flask na porta 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
