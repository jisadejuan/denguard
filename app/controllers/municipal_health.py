
from flask import Blueprint, render_template
from flask_login import login_required, current_user

municipal_health_bp = Blueprint('municipal_health', __name__)


@municipal_health_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Municipal Health Office':
        return "Unauthorized", 403

    return render_template('dashboard/municipal_health_dashboard.html')
