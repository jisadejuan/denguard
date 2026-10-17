from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User

admin = Blueprint('admin', __name__)
admin_bp = admin


@admin.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Administrator':
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    pending_users = User.query.filter_by(is_approved=False).all()

    return render_template(
        'admin/admin_dashboard.html',
        pending_users=pending_users
    )


@admin.route('/approve/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    if current_user.role != 'Administrator':
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)

    if user.role == 'Administrator':
        flash('Administrator accounts cannot be approved through this page.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    user.is_approved = True

    try:
        db.session.commit()
        flash(f'{user.full_name} has been approved successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Failed to approve user. Please try again.', 'danger')

    return redirect(url_for('admin.admin_dashboard'))
