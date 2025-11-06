import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# FichierReglement
# ------------------------
class FichierReglement(db.Model):
    __tablename__ = "fichiers_reglement"
    __fillables__ = ["date_fichier", "utilisateur_id"]
    __showables__= ["date_fichier", "utilisateur_id" ]
    __rel_showables__= ["utilisateur", "fournisseur"]

    id = db.Column(db.Integer, primary_key=True)
    #fournisseur = db.Column(db.String(255), nullable=False)   # ex: "Airtel Money"
    date_fichier = db.Column(Date, nullable=False)
    montant_total = db.Column(Numeric(14,2), default=0)
    nombre_lignes = db.Column(db.Integer, default=0)
    # on peut stocker le fichier brut si besoin: fichier_blob = db.Column(db.LargeBinary)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey("fournisseurs.id"), nullable=True)
    fournisseur = db.relationship("Fournisseur", back_populates="fichiers")
    
    
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("User", back_populates="fichiers")
    

    lignes = db.relationship("LigneReglement", back_populates="fichier", cascade="all, delete-orphan")
    
    def getWording(self) :
        if self.utilisateur :
            return self.utilisateur.getWording() + " " + str(self.date_fichier)
        return self.utilisateur.id + " " + str(self.date_fichier)
