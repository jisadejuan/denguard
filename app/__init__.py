
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'unisan-dengue-tracking-secret-key-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://web_app:strongpassword@localhost/dengue_auth'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in first to access this page.'
    login_manager.login_message_category = 'warning'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Import controllers
    from app.controllers.auth import auth_bp
    from app.controllers.admin import admin_bp
    from app.controllers.health_worker import health_worker_bp
    from app.controllers.barangay_official import barangay_official_bp
    from app.controllers.municipal_health import municipal_health_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(health_worker_bp, url_prefix='/health-worker')
    app.register_blueprint(barangay_official_bp, url_prefix='/barangay-official')
    app.register_blueprint(municipal_health_bp, url_prefix='/municipal-health')

    return app
