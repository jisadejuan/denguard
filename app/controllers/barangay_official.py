
from flask import Blueprint, render_template
from flask_login import login_required, current_user

barangay_official_bp = Blueprint('barangay_official', __name__)


@barangay_official_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Barangay Official':
        return "Unauthorized", 403

    return render_template('dashboard/barangay_official_dashboard.html')
