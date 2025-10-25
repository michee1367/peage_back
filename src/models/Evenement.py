import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# Evenement (UUID) -> journal immuable
# ------------------------
class Evenement(db.Model):
    __tablename__ = "evenements"
    __fillables__ = ["type", "donnees", "date_creation", "transaction_id"]
    __rel_showables__= ["transaction"]
    __showables__= ["type", "donnees", "date_creation"]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.String(100), nullable=False)   # ex: "paiement.initie", "barriere.ouverte"
    donnees = db.Column(JSONB)
    date_creation = db.Column(DateTime, default=func.now())
    hash_precedent = db.Column(db.String(128))
    hash_actuel = db.Column(db.String(128))

    transaction_id = db.Column(UUID(as_uuid=True), db.ForeignKey("transactions.id"), nullable=True)
    transaction = db.relationship("Transaction", back_populates="evenements")
    
    
    def getWording(self) :
        return self.type 
