import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
from datetime import datetime, timezone
# ------------------------
# PassageVehicule (reconciliation)
# ------------------------
class PassageVehicule(db.Model):
    __tablename__ = "passage_vehicules"
    __fillables__ = ["plaque", "transaction_id"]
    __showables__= ["plaque", "transaction_id"]
    __rel_showables__= ["transaction"]

    id = db.Column(db.Integer, primary_key=True)
    plaque = db.Column(db.String(50))
    transaction_id = db.Column(UUID(as_uuid=True), db.ForeignKey("transactions.id"), nullable=True)
    
    creer_a = db.Column("created_at",db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    supprimer_a = db.Column("deleted_at",db.DateTime, nullable=True)

    # relation vers transaction
    transaction = db.relationship("Transaction", back_populates="passages")

    
    def getWording(self) :
        if self.transaction :
            return self.transaction.getWording() + "(" + self.creer_a + ")"
        return "(" + self.id + " " + self.creer_a + ")"

