import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# Tarif
# ------------------------
class Tarif(db.Model):
    __tablename__ = "tarifs"
    __fillables__ = ["devise", "montant", "date_debut_validite", "date_fin_validite", "categorie_id"]
    __showables__= ["devise", "montant", "date_debut_validite", "date_fin_validite"]
    __rel_showables__= ["categorie"]

    id = db.Column(db.Integer, primary_key=True)
    devise_id = db.Column(db.Integer, db.ForeignKey("devises.id"), nullable=False)
    devise = db.relationship("Devise")
    montant = db.Column(Numeric(14, 2), nullable=False)
    date_debut_validite = db.Column(Date)
    date_fin_validite = db.Column(Date)

    categorie_id = db.Column(db.Integer, db.ForeignKey("categories_vehicules.id"), nullable=False)
    categorie = db.relationship("CategorieVehicule", back_populates="tarifs")
    
    
    def getWording(self) :
        if self.categorie :
            return self.categorie.getWording() +  "(" + str(self.date_debut_validite) + ")"
        return str(self.id) + "(" + str(self.date_debut_validite) + ")"
