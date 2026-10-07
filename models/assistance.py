 from app import db


class AssistanceRequest(db.Model):
    __tablename__ = "assistance_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    passenger_id = db.Column(
        db.Integer,
        db.ForeignKey("passengers.id"),
        nullable=False
    )

    request_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    resolved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    passenger = db.relationship(
        "Passenger",
        back_populates="assistance_requests"
    )

    def __repr__(self):
        return f"<AssistanceRequest {self.id}>"
    
