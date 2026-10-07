 from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from app import db
from models.user import User
from models.passenger import Passenger


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            if user.role == "staff":
                return redirect(url_for("staff.dashboard"))

            elif user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            else:
                return redirect(url_for("passenger.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        age = request.form.get("age", type=int)

        assistance_required = (
            request.form.get("assistance_required") == "yes"
        )

        assistance_type = request.form.get(
            "assistance_type",
            ""
        ).strip()

        mobility_required = (
            request.form.get("mobility_required") == "yes"
        )

        connection_minutes = request.form.get(
            "connection_minutes",
            type=int
        )

        if not name or not email or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return render_template("register.html")

        if age is None:
            age = 18

        if connection_minutes is None:
            connection_minutes = 120

        user = User(
            name=name,
            email=email,
            role="passenger"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        passenger = Passenger(
            user_id=user.id,
            age=age,
            assistance_required=assistance_required,
            assistance_type=assistance_type
            if assistance_type else None,
            mobility_required=mobility_required,
            connection_minutes=connection_minutes
        )

        db.session.add(passenger)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/logout")
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("main.home"))

