from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)

    # NOTE: Later we’ll move secret key + DB URL to environment variables.
    app.config["SECRET_KEY"] = "dev-secret-key-change-me"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Import models so SQLAlchemy sees them (IMPORTANT)
    from app.models import User, Vendor  # noqa: F401

    # Register blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    # Routes
    @app.route("/")
    def home():
        return redirect(url_for("dashboard"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        if current_user.role in ("store_admin", "store_staff"):
            return render_template("store/dashboard.html", user=current_user)
        return render_template("vendor/dashboard.html", user=current_user)

    # Create DB tables + bootstrap admin (dev convenience)
    with app.app_context():
        db.create_all()
        _bootstrap_admin_user()

    return app


def _bootstrap_admin_user():
    """
    Dev-only convenience:
    If no users exist, create a default store admin.
    """
    from app.models import User

    if User.query.count() == 0:
        admin = User(
            username="admin",
            role="store_admin",
            email=None,
            is_active=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
from flask_migrate import Migrate