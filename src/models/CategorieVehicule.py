import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# CategorieVehicule
# ------------------------
class CategorieVehicule(db.Model):
    __tablename__ = "categories_vehicules"
    __fillables__ = ["nom", "regle"]
    __showables__= ["nom", "regle"]

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    regle = db.Column(JSONB)   # JSON décrivant la règle (ex: {"essieux":2, "poids_max":3500})

    tarifs = db.relationship("Tarif", back_populates="categorie", cascade="all, delete-orphan")
    
    
    def getWording(self) :
        return self.nom
