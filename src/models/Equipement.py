import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db

# ------------------------
# Equipement
# ------------------------
class Equipement(db.Model):
    __tablename__ = "equipements"
    __fillables__ = ["denomination","type", "numero_serie", "statut", "derniere_communication", "poste_id", "carateristique"]
    __rel_showables__= ["poste"]
    __showables__= ["denomination", "type", "numero_serie", "statut", "derniere_communication", "carateristique"]

    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.String(100)) 
    carateristique = db.Column(db.String(100))                # ex: "POS", "Caméra", "Barrière"
    type = db.Column(db.String(100))                # ex: "POS", "Caméra", "Barrière"
    numero_serie = db.Column(db.String(255), unique=True)
    statut = db.Column(db.String(50))
    derniere_communication = db.Column(DateTime)

    poste_id = db.Column(db.Integer, db.ForeignKey("postes_de_peage.id"), nullable=False)
    poste = db.relationship("PosteDePeage", back_populates="equipements")
    
    def getWording(self) :
        return self.denomination
