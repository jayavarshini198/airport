 from app import db


class Baggage(db.Model):
    __tablename__ = "baggage"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    baggage_tag = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    passenger_id = db.Column(
        db.Integer,
        db.ForeignKey("passengers.id"),
        nullable=False
    )

    flight_id = db.Column(
        db.Integer,
        db.ForeignKey("flights.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Checked In"
    )

    priority_score = db.Column(
        db.Integer,
        default=0
    )

    priority_level = db.Column(
        db.String(20),
        default="NORMAL"
    )

    eta_minutes = db.Column(
        db.Integer,
        default=10
    )

    delay_risk = db.Column(
        db.String(20),
        default="LOW"
    )

    last_updated = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    passenger = db.relationship(
        "Passenger",
        back_populates="baggage"
    )

    flight = db.relationship(
        "Flight",
        back_populates="baggage"
    )

    def __repr__(self):
        return f"<Baggage {self.baggage_tag}>"
    
