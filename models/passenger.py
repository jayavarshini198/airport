 from app import db


class Passenger(db.Model):
    __tablename__ = "passengers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False,
        default=18
    )

    assistance_required = db.Column(
        db.Boolean,
        default=False
    )

    assistance_type = db.Column(
        db.String(100),
        nullable=True
    )

    mobility_required = db.Column(
        db.Boolean,
        default=False
    )

    connection_minutes = db.Column(
        db.Integer,
        default=120
    )

    priority_score = db.Column(
        db.Integer,
        default=0
    )

    priority_level = db.Column(
        db.String(20),
        default="NORMAL"
    )

    user = db.relationship(
        "User",
        back_populates="passenger"
    )

    baggage = db.relationship(
        "Baggage",
        back_populates="passenger",
        cascade="all, delete-orphan"
    )

    assistance_requests = db.relationship(
        "AssistanceRequest",
        back_populates="passenger",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Passenger {self.id}>"
    

     