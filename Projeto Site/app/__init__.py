from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os



db = SQLAlchemy()


def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'minha-chave-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .models import Usuario
        from .models.teste_aptidao import TesteAptidao
        from app.models.administrador import Administrador
        from app.models.centro_adocao import CentroAdocao
        from app.models.produto import Produto, Venda, ItemVenda

        db.create_all()

        
        from app.routes.auth import auth_bp
        from app.routes.admin import admin_bp
        from app.routes.usuario import usuario_bp
        from app.routes.teste import teste_bp
        from app.routes.centros import centros_bp
        from app.routes.loja import loja_bp


        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(usuario_bp)
        app.register_blueprint(teste_bp)
        app.register_blueprint(centros_bp)
        app.register_blueprint(loja_bp)
    return app
