from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from models.baggage import Baggage
from models.flight import Flight
from models.assistance import AssistanceRequest

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health")
def health():
    return jsonify({
        "status": "success",
        "message": "Smart Airport API is running"
    })


@api.route("/baggage/<int:baggage_id>")
@login_required
def baggage_status(baggage_id):
    baggage = Baggage.query.get_or_404(baggage_id)

    return jsonify({
        "id": baggage.id,
        "baggage_tag": baggage.baggage_tag,
        "status": baggage.status,
        "priority_score": baggage.priority_score,
        "priority_level": baggage.priority_level,
        "eta_minutes": baggage.eta_minutes,
        "delay_risk": baggage.delay_risk
    })


@api.route("/flights")
@login_required
def flights():
    flights = Flight.query.all()

    data = []

    for flight in flights:
        data.append({
            "id": flight.id,
            "flight_number": flight.flight_number,
            "source": flight.source,
            "destination": flight.destination,
            "departure_time": str(flight.departure_time)
            if flight.departure_time else None
        })

    return jsonify(data)


@api.route("/assistance")
@login_required
def assistance_requests():
    requests = AssistanceRequest.query.order_by(
        AssistanceRequest.created_at.desc()
    ).all()

    data = []

    for request in requests:
        data.append({
            "id": request.id,
            "request_type": request.request_type,
            "description": request.description,
            "status": request.status,
            "created_at": str(request.created_at)
        })

    return jsonify(data)
