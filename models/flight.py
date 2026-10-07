 from app import db


class Flight(db.Model):
    __tablename__ = "flights"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    flight_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    source = db.Column(
        db.String(100),
        nullable=False
    )

    destination = db.Column(
        db.String(100),
        nullable=False
    )

    departure_time = db.Column(
        db.DateTime,
        nullable=True
    )

    arrival_time = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="Scheduled"
    )

    baggage = db.relationship(
        "Baggage",
        back_populates="flight"
    )

    def __repr__(self):
        return f"<Flight {self.flight_number}>"