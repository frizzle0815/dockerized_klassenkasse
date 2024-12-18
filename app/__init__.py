from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    with app.app_context():
        # Import models after db initialization
        from app.models import User
        
        # Import and register blueprints
        from app.routes import main
        from app.admin_routes import admin
        
        app.register_blueprint(main)
        app.register_blueprint(admin, url_prefix='/admin')
        
        # Create database tables
        db.create_all()

        # Setup login manager
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
