import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# Transaction (UUID)
# ------------------------
class Versement(db.Model):
    __tablename__ = "versements"
    __rel_showables__= ["quart", "utilisateur", "devise"]
    __fillables__ = ["devise_id", "montant", "date_confirmation", "quart_id", "utilisateur_id"]
    __showables__= ["devise_id", "montant", "date_creation", "date_confirmation", "quart_id", "utilisateur_id"]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    montant = db.Column(Numeric(14,2), nullable=False)
    devise_id = db.Column(db.Integer, db.ForeignKey("devises.id"), nullable=False)
    devise = db.relationship("Devise")      # immatriculation, si disponible
    date_creation = db.Column(DateTime, default=func.now())
    date_confirmation = db.Column(DateTime)

    # Liens
    
    quart_id = db.Column(db.Integer, db.ForeignKey("quarts_de_travail.id"), nullable=True)
    quart = db.relationship("QuartDeTravail", back_populates="versements")
    
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("User", back_populates="versements")
    
    def getWording(self) :
        if self.quart :
            return str(self.quart.getWording()) + "(" + str(self.date_creation) + " - " + str(self.id) + ")"
        return str(self.date_creation) + "(" + str(self.id) + ")"
