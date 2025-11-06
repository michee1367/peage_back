import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# QuartDeTravail
# ------------------------
class QuartDeTravail(db.Model):
    __tablename__ = "quarts_de_travail"
    __rel_showables__= ["poste", "utilisateur", "versement"]
    __fillables__ = ["heure_ouverture", "heure_fermeture", "montant_cloture", "poste_id", "utilisateur_id"]
    __showables__= ["heure_ouverture", "heure_fermeture", "montant_cloture", "utilisateur_id"]

    id = db.Column(db.Integer, primary_key=True)
    heure_ouverture = db.Column(DateTime, default=func.now())
    heure_fermeture = db.Column(DateTime)
    fond_ouverture = db.Column(Numeric(14,2), default=0)
    montant_cloture = db.Column(Numeric(14,2))
    
    poste_id = db.Column(db.Integer, db.ForeignKey("postes_de_peage.id"), nullable=False)
    poste = db.relationship("PosteDePeage", back_populates="quarts")
    
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("User", back_populates="quarts")

    transactions = db.relationship("Transaction", back_populates="quart", cascade="all, delete-orphan")
    versements = db.relationship("Versement", back_populates="quart", cascade="all, delete-orphan")
    
    
    def getWording(self) :
        if self.utilisateur :
            return self.utilisateur.getWording() + "(" + str(self.heure_ouverture) + ')'
        return str(self.id) + "(" + str(self.heure_ouverture) + ')'
