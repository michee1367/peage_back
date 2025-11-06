import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# Transaction (UUID)
# ------------------------
class Transaction(db.Model):
    __tablename__ = "transactions"
    __rel_showables__= ["quart", "categorie", "devise"]
    __fillables__ = ["devise_id", "montant", "moyen_paiement", 
                     "statut", "plaque", "date_confirmation", 
                     "reference_externe", "quart_id", "categorie_id"]
    __showables__= ["devise_id", "montant", "moyen_paiement", "statut", "plaque", "date_creation", "date_confirmation", "reference_externe", "categorie_id"]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    montant = db.Column(Numeric(14,2), nullable=False)
    devise_id = db.Column(db.Integer, db.ForeignKey("devises.id"), nullable=False)
    devise = db.relationship("Devise")
    moyen_paiement = db.Column(db.String(50))   # ex: "espece", "mobile_money", "carte"
    statut = db.Column(db.String(50), default="en_attente")  # en_attente, confirme, annule, echec
    plaque = db.Column(db.String(50))            # immatriculation, si disponible
    date_creation = db.Column(DateTime, default=func.now())
    date_confirmation = db.Column(DateTime)
    reference_externe = db.Column(db.String(255), index=True)  # ref fournie par prestataire externe (si existant)

    # Liens
    quart_id = db.Column(db.Integer, db.ForeignKey("quarts_de_travail.id"), nullable=True)
    quart = db.relationship("QuartDeTravail", back_populates="transactions")

    categorie_id = db.Column(db.Integer, db.ForeignKey("categories_vehicules.id"), nullable=False)
    categorie = db.relationship("CategorieVehicule", back_populates="transactions")

    evenements = db.relationship("Evenement", back_populates="transaction", cascade="all, delete-orphan")
    
    # lien optionnel vers LigneReglement (reconciliation)
    ligne_reglement = db.relationship("LigneReglement", back_populates="transaction", uselist=False)
    
    
    def getWording(self) :
        return str(self.plaque) + "(" + str(self.date_creation) + " - " + str(self.id) + ")"
