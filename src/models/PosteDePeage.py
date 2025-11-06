import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# Poste de péage
# ------------------------
class PosteDePeage(db.Model):
    __tablename__ = "postes_de_peage"
    __rel_showables__= ["route"]
    __fillables__ = ["nom", "localisation", "date_creation", "route_id"]
    __showables__= ["nom", "localisation", "date_creation"]

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    localisation = db.Column(db.String(512))
    date_creation = db.Column(DateTime, default=func.now())
    
    
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    route = db.relationship("Route", back_populates="postes")

    quarts = db.relationship("QuartDeTravail", back_populates="poste", cascade="all, delete-orphan")
    equipements = db.relationship("Equipement", back_populates="poste", cascade="all, delete-orphan")
    collectes = db.relationship("Collecte", back_populates="poste", cascade="all, delete-orphan")
    
        
    def getWording(self) :
        return self.nom 

