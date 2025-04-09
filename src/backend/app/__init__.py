from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Inicialização das extensões
db = SQLAlchemy()

def create_app(config=None):
    """Função fábrica da aplicação Flask."""
    app = Flask(__name__)
    
    # Configuração padrão
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///misa_cash.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    # Sobrescreve com configuração passada como parâmetro
    if config:
        app.config.from_mapping(config)
    
    # Inicializa extensões
    CORS(app)
    db.init_app(app)
    
    # Registra blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Comando para inicializar o banco de dados
    @app.cli.command('init-db')
    def init_db_command():
        """Limpa os dados existentes e cria novas tabelas."""
        db.drop_all()
        db.create_all()
        print('Banco de dados inicializado.')
    
    return app 