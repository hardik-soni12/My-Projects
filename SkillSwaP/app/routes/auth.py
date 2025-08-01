from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms import RegistrationForm, LoginForm
from app import db

auth_bp = Blueprint('auth_bp', __name__)


# registration route

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():

        # Check if email or username already exists
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()

        if existing_user:
            flash('Username or Email already exists', 'danger')
            return redirect(url_for('auth_bp.register'))
        
        user = User( username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration Successful, You can now log in.', 'success')
        return redirect(url_for('auth_bp.login'))
    
    return render_template('register.html', form = form)



# Login Route

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(email = form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully.', 'success')
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html', form = form)


# logout route

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth_bp.login'))


# dashboard route protected

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user = current_user)