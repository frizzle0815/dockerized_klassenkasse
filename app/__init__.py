from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import User  # Importiere User für den User-Loader

# Erstelle Flask-App und konfiguriere sie
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialisiere Erweiterungen
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

# Registriere Blueprints
from app.routes import main
from app.admin_routes import admin

app.register_blueprint(main)
app.register_blueprint(admin, url_prefix='/admin')

# Login-Manager User-Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))