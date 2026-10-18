
from flask import Blueprint, render_template
from flask_login import login_required, current_user

health_worker_bp = Blueprint('health_worker', __name__)


@health_worker_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Health Worker':
        return "Unauthorized", 403

    return render_template('dashboard/health_worker_dashboard.html')
