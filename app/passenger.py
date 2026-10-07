 from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from models.passenger import Passenger
from models.baggage import Baggage
from models.assistance import AssistanceRequest
from services.priority_engine import calculate_priority
from services.prediction_engine import predict_baggage


passenger = Blueprint("passenger", __name__, url_prefix="/passenger")


@passenger.route("/dashboard")
@login_required
def dashboard():

    passenger_profile = Passenger.query.filter_by(
        user_id=current_user.id
    ).first()

    if not passenger_profile:
        flash("Passenger profile not found.", "danger")
        return redirect(url_for("main.home"))

    # Recalculate priority score
    result = calculate_priority(passenger_profile)

    passenger_profile.priority_score = result["score"]
    passenger_profile.priority_level = result["level"]

    db.session.commit()

    baggage_list = Baggage.query.filter_by(
        passenger_id=passenger_profile.id
    ).all()

    return render_template(
        "passenger/dashboard.html",
        passenger=passenger_profile,
        baggage_list=baggage_list
    )


@passenger.route("/baggage")
@login_required
def baggage():

    passenger_profile = Passenger.query.filter_by(
        user_id=current_user.id
    ).first()

    if not passenger_profile:
        flash("Passenger profile not found.", "danger")
        return redirect(url_for("main.home"))

    baggage_list = Baggage.query.filter_by(
        passenger_id=passenger_profile.id
    ).all()

    return render_template(
        "passenger/baggage.html",
        baggage_list=baggage_list
    )


@passenger.route("/baggage/<int:baggage_id>")
@login_required
def baggage_details(baggage_id):

    passenger_profile = Passenger.query.filter_by(
        user_id=current_user.id
    ).first()

    baggage = Baggage.query.get_or_404(baggage_id)

    # Prevent passengers from viewing another passenger's baggage
    if baggage.passenger_id != passenger_profile.id:
        flash("You are not authorized to view this baggage.", "danger")
        return redirect(url_for("passenger.baggage"))

    prediction = predict_baggage(baggage.status)

    baggage.eta_minutes = prediction["eta_minutes"]
    baggage.delay_risk = prediction["delay_risk"]

    db.session.commit()

    return render_template(
        "passenger/baggage.html",
        baggage=baggage,
        prediction=prediction,
        baggage_list=[baggage]
    )


@passenger.route("/assistance", methods=["GET", "POST"])
@login_required
def assistance():

    passenger_profile = Passenger.query.filter_by(
        user_id=current_user.id
    ).first()

    if not passenger_profile:
        flash("Passenger profile not found.", "danger")
        return redirect(url_for("main.home"))

    if request.method == "POST":

        request_type = request.form.get(
            "request_type",
            "General Assistance"
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        assistance_request = AssistanceRequest(
            passenger_id=passenger_profile.id,
            request_type=request_type,
            description=description,
            status="Pending"
        )

        db.session.add(assistance_request)
        db.session.commit()

        flash(
            "Assistance request submitted successfully.",
            "success"
        )

        return redirect(
            url_for("passenger.assistance")
        )

    requests = AssistanceRequest.query.filter_by(
        passenger_id=passenger_profile.id
    ).order_by(
        AssistanceRequest.created_at.desc()
    ).all()

    return render_template(
        "passenger/assistance.html",
        requests=requests
    )


@passenger.route("/notifications")
@login_required
def notifications():

    return render_template(
        "passenger/notifications.html"
    )
