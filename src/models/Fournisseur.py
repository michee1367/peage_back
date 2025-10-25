
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db

# ------------------------
# Caissier
# ------------------------
class Fournisseur(db.Model):
    __tablename__ = "fournisseurs"
    __fillables__ = ["nom", "identifiant"]
    __showables__= ["nom", "identifiant"]

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    identifiant = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(512), nullable=False)

    fichiers = db.relationship("FichierReglement", back_populates="fournisseur")
    
    def getWording(self) :
        return self.nom 
