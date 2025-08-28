from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms import RegistrationForm, LoginForm
from app import db , mail
from flask_mail import Message
from app.utils.token import generate_token, verify_token

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/')
def home():
    return redirect(url_for('auth_bp.login'))

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

        # email verification

        token = generate_token(user.email)
        verify_url = url_for('auth_bp.verify_email', token = token, _external= True)

        msg = Message('Email Verification',recipients=[user.email])
        msg.body = f'Click the link to verify your email: {verify_url}'
        mail.send(msg)

        flash('Registration Successful, You can now log in.', 'success')
        return redirect(url_for('auth_bp.login'))
    
    return render_template('register.html', form = form)



# Email verification route

@auth_bp.route('/verify/<token>')
def verify_email(token):
    email = verify_token(token)
    if not email:
        flash('verification link is invalid or expired.','danger')
        return redirect(url_for('auth_bp.login'))
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('Account Already verified.','info')
    else:
        user.is_verified = True
        db.session.commit()
        flash('Email verification successfull. you can log in now.','success')
    return redirect(url_for('auth_bp.login'))


#notice route

@auth_bp.route('/verify-email')
@login_required
def verify_email_notice():
    if current_user.is_verified:
        return redirect(url_for('auth_bp.dashboard'))
    return render_template('verify_email.html', user=current_user)



# Login Route

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        if current_user.is_verified:
            return redirect(url_for('auth_bp.dashboard'))
        else:
            return redirect(url_for('auth_bp.verify_email_notice'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            if not user.is_verified:
                flash('Please verify your email before accessing all features.', 'warning')
                return redirect(url_for('auth_bp.verify_email_notice'))
            flash('Logged in Successfully.', 'success')
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html', form=form)


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
    if not current_user.is_verified:
        flash('Please verify your email first.','danger')
        return redirect(url_for('auth_bp.login'))
    return render_template('dashboard.html', user = current_user, skills = current_user.skills)