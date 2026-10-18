
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User

admin = Blueprint('admin', __name__)
admin_bp = admin


def admin_required():
    return current_user.is_authenticated and current_user.role == 'Administrator'


@admin.route('/dashboard')
@login_required
def admin_dashboard():
    if not admin_required():
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
    if not admin_required():
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)

    if user.role == 'Administrator':
        flash('Administrator accounts cannot be approved through this page.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    if user.is_approved:
        flash('This account has already been approved.', 'info')
        return redirect(url_for('admin.admin_dashboard'))

    user.is_approved = True

    try:
        db.session.commit()
        flash(f'{user.full_name} has been approved successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Failed to approve user. Please try again.', 'danger')

    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/users')
@login_required
def manage_users():
    if not admin_required():
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    users = User.query.order_by(User.id.desc()).all()

    return render_template(
        'admin/manage_users.html',
        users=users
    )


@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not admin_required():
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('You cannot remove your own Administrator account.', 'warning')
        return redirect(url_for('admin.manage_users'))

    if user.role == 'Administrator':
        flash('Administrator accounts cannot be removed through this page.', 'warning')
        return redirect(url_for('admin.manage_users'))

    try:
        name = user.full_name
        db.session.delete(user)
        db.session.commit()
        flash(f'{name} has been removed successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('Failed to remove user. Check whether this account has related records.', 'danger')

    return redirect(url_for('admin.manage_users'))
