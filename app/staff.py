from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from models.baggage import Baggage
from models.assistance import AssistanceRequest
from services.prediction_engine import predict_baggage


staff = Blueprint("staff", __name__, url_prefix="/staff")


@staff.before_request
@login_required
def restrict_to_staff():
    if current_user.role != "staff":
        flash("Staff access only.", "danger")
        return redirect(url_for("main.home"))


@staff.route("/dashboard")
def dashboard():

    baggage_list = Baggage.query.order_by(
        Baggage.priority_score.desc()
    ).all()

    assistance_requests = AssistanceRequest.query.order_by(
        AssistanceRequest.created_at.desc()
    ).all()

    return render_template(
        "staff/dashboard.html",
        baggage_list=baggage_list,
        assistance_requests=assistance_requests
    )


@staff.route("/baggage")
def baggage():

    baggage_list = Baggage.query.order_by(
        Baggage.priority_score.desc()
    ).all()

    return render_template(
        "staff/baggage.html",
        baggage_list=baggage_list
    )


@staff.route("/baggage/<int:baggage_id>/update", methods=["POST"])
def update_baggage(baggage_id):

    baggage = Baggage.query.get_or_404(baggage_id)

    new_status = request.form.get("status", "").strip()

    allowed_statuses = [
        "Checked In",
        "Processing",
        "Loaded",
        "Arrived",
        "Claim Ready",
        "Collected"
    ]

    if new_status not in allowed_statuses:
        flash("Invalid baggage status.", "danger")
        return redirect(url_for("staff.baggage"))

    baggage.status = new_status

    prediction = predict_baggage(new_status)

    baggage.eta_minutes = prediction["eta_minutes"]
    baggage.delay_risk = prediction["delay_risk"]

    db.session.commit()

    flash(
        f"Baggage {baggage.baggage_tag} updated successfully.",
        "success"
    )

    return redirect(url_for("staff.baggage"))


@staff.route("/assistance")
def assistance():

    requests = AssistanceRequest.query.order_by(
        AssistanceRequest.created_at.desc()
    ).all()

    return render_template(
        "staff/assistance.html",
        requests=requests
    )


@staff.route("/assistance/<int:request_id>/update", methods=["POST"])
def update_assistance(request_id):

    assistance_request = AssistanceRequest.query.get_or_404(
        request_id
    )

    new_status = request.form.get("status", "").strip()

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        flash("Invalid assistance status.", "danger")
        return redirect(url_for("staff.assistance"))

    assistance_request.status = new_status

    if new_status == "Resolved":
        assistance_request.resolved_at = db.func.now()

    db.session.commit()

    flash(
        "Assistance request updated successfully.",
        "success"
    )

    return redirect(url_for("staff.assistance"))
 
