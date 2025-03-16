from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dotenv import DotEnv
from flask_login import LoginManager
from loguru import logger
import os

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
env = DotEnv()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
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
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
