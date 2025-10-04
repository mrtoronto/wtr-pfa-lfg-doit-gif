from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.db.user import User
import logging

logger = logging.getLogger('APP')
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', title='Home')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', title='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate inputs
        if not username or not password:
            flash('Username and password are required')
            return render_template('register.html', title='Register')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html', title='Register')
        
        # Create new user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        logger.info(f'New user registered: {username}')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register')

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'change_username':
            new_username = request.form.get('new_username')
            
            if not new_username:
                flash('Username cannot be empty')
                return render_template('settings.html', title='Settings')
            
            # Check if username already exists
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Username already taken')
                return render_template('settings.html', title='Settings')
            
            old_username = current_user.username
            current_user.username = new_username
            db.session.commit()
            logger.info(f'User {old_username} changed username to {new_username}')
            flash('Username updated successfully!')
        
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_password or not new_password or not confirm_password:
                flash('All password fields are required')
                return render_template('settings.html', title='Settings')
            
            if not current_user.check_password(current_password):
                flash('Current password is incorrect')
                return render_template('settings.html', title='Settings')
            
            if new_password != confirm_password:
                flash('New passwords do not match')
                return render_template('settings.html', title='Settings')
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters')
                return render_template('settings.html', title='Settings')
            
            current_user.set_password(new_password)
            db.session.commit()
            logger.info(f'User {current_user.username} changed their password')
            flash('Password updated successfully!')
    
    return render_template('settings.html', title='Settings')

