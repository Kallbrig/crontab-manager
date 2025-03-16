import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dotenv import DotEnv
from flask_login import LoginManager
from loguru import logger

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
env = DotEnv()
login = LoginManager()
login.login_view = 'auth.login'

# Import models here after db is defined
from models import User, CronJob  # noqa: F401

def create_app():
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for development

    # Initialize extensions
    db.init_app(app)
    env.init_app(app)
    login.init_app(app)

    # Configure logging
    logger.add("logs/app.log", rotation="500 MB", retention="10 days")

    # Register blueprints
    from routes import main
    from auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
