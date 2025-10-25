
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db

# ------------------------
# Caissier
# ------------------------
class Caissier(db.Model):
    __tablename__ = "caissiers"
    __fillables__ = ["nom", "identifiant"]
    __showables__= ["nom", "identifiant"]

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    identifiant = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(50), default="caissier")
    
    def getWording(self) :
        return self.nom

