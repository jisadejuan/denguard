from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

# Initialize Blueprint (Siguraduhing auth_bp o auth ang gamit)
auth = Blueprint('auth', __name__)
auth_bp = auth  # Para sa compatibility sa __init__.py kung auth_bp ang gamit doon

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_approved and user.role != 'Admin':
            flash('Your account is pending for Admin approval. Please wait for confirmation.', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user)

        if user.role == 'Admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            # Pansamantalang redirection habang ginagawa pa ang public dashboard
            flash('Login successful! Welcome to the system.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('public/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        barangay = request.form.get('barangay')
        contact_number = request.form.get('contact_number')

        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email address is already registered. Please use another email or log in.', 'danger')
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(
            full_name=full_name,
            email=email,
            role=role,
            barangay=barangay,
            contact_number=contact_number,
            is_approved=False
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please wait for Admin approval before logging in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('public/register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))