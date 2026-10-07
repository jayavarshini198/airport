 from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from models.user import User
from models.passenger import Passenger
from models.flight import Flight
from models.baggage import Baggage


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
@login_required
def restrict_to_admin():
    if current_user.role != "admin":
        flash("Admin access only.", "danger")
        return redirect(url_for("main.home"))


@admin.route("/dashboard")
def dashboard():

    total_users = User.query.count()
    total_passengers = Passenger.query.count()
    total_flights = Flight.query.count()
    total_baggage = Baggage.query.count()

    high_priority = Baggage.query.filter_by(
        priority_level="HIGH"
    ).count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_passengers=total_passengers,
        total_flights=total_flights,
        total_baggage=total_baggage,
        high_priority=high_priority
    )


@admin.route("/users")
def users():

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )


@admin.route("/flights")
def flights():

    flights = Flight.query.order_by(
        Flight.departure_time.asc()
    ).all()

    return render_template(
        "admin/flights.html",
        flights=flights
    )


@admin.route("/flight/add", methods=["GET", "POST"])
def add_flight():

    if request.method == "POST":

        flight_number = request.form.get(
            "flight_number", ""
        ).strip()

        source = request.form.get(
            "source", ""
        ).strip()

        destination = request.form.get(
            "destination", ""
        ).strip()

        if not flight_number or not source or not destination:
            flash(
                "Flight number, source and destination are required.",
                "danger"
            )
            return render_template("admin/add_flight.html")

        if Flight.query.filter_by(
            flight_number=flight_number
        ).first():

            flash(
                "A flight with this number already exists.",
                "warning"
            )
            return render_template("admin/add_flight.html")

        flight = Flight(
            flight_number=flight_number,
            source=source,
            destination=destination,
            status="Scheduled"
        )

        db.session.add(flight)
        db.session.commit()

        flash(
            "Flight added successfully.",
            "success"
        )

        return redirect(
            url_for("admin.flights")
        )

    return render_template(
        "admin/add_flight.html"
    )

