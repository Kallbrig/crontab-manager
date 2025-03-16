from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import User, CronJob
from app import db
from loguru import logger
from datetime import datetime

# Create blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page route"""
    return render_template('index.html', title='Home')

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page route"""
    cron_jobs = CronJob.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', cron_jobs=cron_jobs)

@main.route('/cron_jobs/create', methods=['POST'])
@login_required
def create_cron_job():
    """Create a new cron job"""
    schedule = request.form.get('schedule')
    command = request.form.get('command')
    enabled = bool(request.form.get('enabled', True))

    if not all([schedule, command]):
        flash('Please fill in all required fields', 'danger')
        return redirect(url_for('main.dashboard'))

    try:
        cron_job = CronJob(
            schedule=schedule,
            command=command,
            enabled=enabled,
            user_id=current_user.id
        )
        db.session.add(cron_job)
        db.session.commit()
        flash('Cron job created successfully', 'success')
    except Exception as e:
        logger.error(f"Error creating cron job: {e}")
        db.session.rollback()
        flash('Error creating cron job', 'danger')

    return redirect(url_for('main.dashboard'))

@main.route('/cron_jobs/<int:job_id>/edit', methods=['POST'])
@login_required
def edit_cron_job(job_id):
    """Edit an existing cron job"""
    cron_job = CronJob.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    
    schedule = request.form.get('schedule')
    command = request.form.get('command')
    enabled = bool(request.form.get('enabled', True))

    if not all([schedule, command]):
        flash('Please fill in all required fields', 'danger')
        return redirect(url_for('main.dashboard'))

    try:
        cron_job.schedule = schedule
        cron_job.command = command
        cron_job.enabled = enabled
        cron_job.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Cron job updated successfully', 'success')
    except Exception as e:
        logger.error(f"Error updating cron job: {e}")
        db.session.rollback()
        flash('Error updating cron job', 'danger')

    return redirect(url_for('main.dashboard'))

@main.route('/cron_jobs/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_cron_job(job_id):
    """Delete a cron job"""
    cron_job = CronJob.query.filter_by(id=job_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(cron_job)
        db.session.commit()
        flash('Cron job deleted successfully', 'success')
    except Exception as e:
        logger.error(f"Error deleting cron job: {e}")
        db.session.rollback()
        flash('Error deleting cron job', 'danger')

    return redirect(url_for('main.dashboard'))

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
