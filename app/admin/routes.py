from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.models import Vendor, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    if not current_user.is_authenticated or current_user.role != "store_admin":
        return False
    return True


@admin_bp.route("/vendors", methods=["GET", "POST"])
@login_required
def manage_vendors():
    if not admin_required():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        if name:
            vendor = Vendor(name=name)
            db.session.add(vendor)
            db.session.commit()
            flash("Vendor created successfully.", "success")

    vendors = Vendor.query.all()
    return render_template("admin/vendors.html", vendors=vendors)


@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
def manage_users():
    if not admin_required():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        vendor_id = request.form.get("vendor_id")

        user = User(username=username.lower(), role=role)
        user.set_password(password)

        if role == "vendor_user":
            user.vendor_id = vendor_id

        db.session.add(user)
        db.session.commit()
        flash("User created successfully.", "success")

    users = User.query.all()
    vendors = Vendor.query.all()

    return render_template("admin/users.html", users=users, vendors=vendors)
