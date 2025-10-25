import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# (Option) Table vehicules pour référencer tags RFID, etc.
# ------------------------
class Vehicule(db.Model):
    __tablename__ = "vehicules"
    __rel_showables__= ["categorie"]
    __fillables__ = ["immatriculation", "tag_rfid", "type_identification", "proprietaire", "categorie_id"]
    __showables__= ["immatriculation", "tag_rfid", "type_identification", "proprietaire"]

    id = db.Column(db.Integer, primary_key=True)
    immatriculation = db.Column(db.String(50), index=True)
    tag_rfid = db.Column(db.String(255), unique=True)
    type_identification = db.Column(db.String(50))   # ex: "LAPI", "RFID", "MANUEL"
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories_vehicules.id"))
    proprietaire = db.Column(db.String(255))

    categorie = db.relationship("CategorieVehicule")
    # Si tu veux lier la transaction au véhicule, ajoute transaction.vehicule_id
    
    def getWording(self) :
        if self.categorie :
            return self.immatriculation + "("+ self.categorie.getWording() +")"
        return self.immatriculation 
