from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    username = (request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Invalid username or password.", "error")
        return render_template("auth/login.html"), 401

    if not user.is_active:
        flash("This account is disabled. Contact admin.", "error")
        return render_template("auth/login.html"), 403

    if not user.check_password(password):
        flash("Invalid username or password.", "error")
        return render_template("auth/login.html"), 401

    login_user(user)
    return redirect(url_for("dashboard"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
