from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User

auth = Blueprint('auth', __name__)
auth_bp = auth

ALLOWED_ROLES = {
    'Health Worker',
    'Barangay Official',
    'Municipal Health Office'
}


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        if user.role != 'Administrator' and not user.is_approved:
            flash(
                'Your account is pending Administrator approval.',
                'warning'
            )
            return redirect(url_for('auth.login'))

        login_user(user)

        if user.role == 'Administrator':
            return redirect(url_for('admin.admin_dashboard'))
        elif user.role == 'Health Worker':
            return redirect(url_for('health_worker.dashboard'))
        elif user.role == 'Barangay Official':
            return redirect(url_for('barangay_official.dashboard'))
    elif user.role == 'Municipal Health Office':
        return redirect(url_for('municipal_health.dashboard'))
    else:
        logout_user()
    flash('Your account role is not recognized.', 'danger')
    return redirect(url_for('auth.login'))

    return render_template('public/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', '')
        barangay = request.form.get('barangay', '').strip()
        contact_number = request.form.get('contact_number', '').strip()

        if not all([
            full_name, email, password,
            confirm_password, role, barangay
        ]):
            flash('Please complete all required fields.', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        if role not in ALLOWED_ROLES:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('This email is already registered.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(
            full_name=full_name,
            email=email,
            role=role,
            barangay=barangay,
            contact_number=contact_number or None,
            is_approved=False
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(
                'Registration successful! Wait for Administrator approval.',
                'success'
            )
            return redirect(url_for('auth.login'))
        except Exception:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('public/register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
