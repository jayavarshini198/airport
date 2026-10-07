from app import create_app, db

from models.user import User
from models.passenger import Passenger
from models.flight import Flight
from models.baggage import Baggage

from services.priority_engine import calculate_priority


app = create_app()


with app.app_context():

    # Passenger account

    user = User.query.filter_by(
        email="passenger@test.com"
    ).first()

    if not user:

        user = User(
            name="Anu Kumar",
            email="passenger@test.com",
            role="passenger"
        )

        user.set_password("pass123")

        db.session.add(user)
        db.session.commit()


    passenger = Passenger.query.filter_by(
        user_id=user.id
    ).first()

    if not passenger:

        passenger = Passenger(
            user_id=user.id,
            age=72,
            assistance_required=True,
            assistance_type="Wheelchair Assistance",
            mobility_requirement=True,
            connection_minutes=45
        )

        db.session.add(passenger)
        db.session.commit()


    # Staff

    staff = User.query.filter_by(
        email="staff@airport.com"
    ).first()

    if not staff:

        staff = User(
            name="Airport Operations",
            email="staff@airport.com",
            role="staff"
        )

        staff.set_password("staff123")

        db.session.add(staff)


    # Admin

    admin = User.query.filter_by(
        email="admin@airport.com"
    ).first()

    if not admin:

        admin = User(
            name="System Administrator",
            email="admin@airport.com",
            role="admin"
        )

        admin.set_password("admin123")

        db.session.add(admin)


    db.session.commit()


    # Flight

    flight = Flight.query.filter_by(
        flight_number="AI452"
    ).first()

    if not flight:

        flight = Flight(
            flight_number="AI452",
            origin="Coimbatore",
            destination="Delhi",
            departure_time="08:30",
            arrival_time="11:30",
            status="Arrived"
        )

        db.session.add(flight)

        db.session.commit()


    # Baggage

    bag = Baggage.query.filter_by(
        baggage_id="BG2026"
    ).first()

    if not bag:

        score, level = calculate_priority(
            passenger.age,
            passenger.assistance_required,
            passenger.mobility_requirement,
            passenger.connection_minutes
        )

        bag = Baggage(
            baggage_id="BG2026",
            passenger_id=passenger.id,
            flight_id=flight.id,
            status="Processing",
            priority_score=score,
            priority_level=level,
            estimated_minutes=8,
            delay_risk="LOW"
        )

        db.session.add(bag)


    db.session.commit()

    print("Sample data created successfully.")
    