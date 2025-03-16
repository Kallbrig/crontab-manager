from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import User
from app import db
from loguru import logger

# Create blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page route"""
    return render_template('index.html', title='Home')

@main.route('/dashboard')
def dashboard():
    """Dashboard page route"""
    return render_template('dashboard.html', title='Dashboard')

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
