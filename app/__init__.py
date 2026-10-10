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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://web_app:DeNgUaRd26!@localhost/sampledb'
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
        return User.query.get(int(user_id))

    # Automatic redirect to login page when visiting root URL
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    from app.controllers.auth import auth_bp
    from app.controllers.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app