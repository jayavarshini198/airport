 from flask import Blueprint, render_template
from flask_login import current_user


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("home.html")


@main.route("/dashboard")
def dashboard():

    if not current_user.is_authenticated:
        return render_template("home.html")

    if current_user.role == "staff":
        return render_template(
            "staff/dashboard.html"
        )

    if current_user.role == "admin":
        return render_template(
            "admin/dashboard.html"
        )

    return render_template(
        "passenger/dashboard.html"
    )
