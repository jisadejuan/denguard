from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User

admin = Blueprint('admin', __name__)
admin_bp = admin  # Para sa compatibility sa app/__init__.py

@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Siguraduhing Admin lang ang makakapasok
    if current_user.role != 'Admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    # Kuhanin ang lahat ng users na pending pa (is_approved == False)
    pending_users = User.query.filter_by(is_approved=False).all()
    return render_template('admin/admin_dashboard.html', pending_users=pending_users)


@admin.route('/admin/approve/<int:user_id>')
@login_required
def approve_user(user_id):
    if current_user.role != 'Admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    user.is_approved = True

    try:
        db.session.commit()
        flash(f'User {user.full_name} has been successfully approved!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to approve user. Please try again.', 'danger')

    return redirect(url_for('admin.admin_dashboard'))