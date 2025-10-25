import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
from datetime import datetime, timezone
# ------------------------
# LigneReglement (reconciliation)
# ------------------------
class LigneReglement(db.Model):
    __tablename__ = "lignes_reglement"
    __fillables__ = ["reference_externe", "montant", "statut", "nombre_lignes", "transaction_id", "fichier_id"]
    __showables__= ["reference_externe", "montant", "statut", "nombre_lignes"]
    __rel_showables__= ["transaction", "fichier"]

    id = db.Column(db.Integer, primary_key=True)
    reference_externe = db.Column(db.String(255), nullable=False, index=True)
    montant = db.Column(Numeric(14,2), nullable=False)
    statut = db.Column(db.String(50))   # ex: "SUCCESS", "FAILED", "PENDING"
    transaction_id = db.Column(UUID(as_uuid=True), db.ForeignKey("transactions.id"), nullable=True)
    
    creer_a = db.Column("created_at",db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    supprimer_a = db.Column("deleted_at",db.DateTime, nullable=True)

    # relation vers transaction
    transaction = db.relationship("Transaction", back_populates="ligne_reglement")

    # relation vers fichier
    fichier_id = db.Column(db.Integer, db.ForeignKey("fichiers_reglement.id"), nullable=False)
    fichier = db.relationship("FichierReglement", back_populates="lignes")

    __table_args__ = (
        UniqueConstraint("fichier_id", "reference_externe", name="uq_fichier_reference"),
    )
    
    def getWording(self) :
        if self.fichier :
            return self.fichier.getWording() + "(" + self.montant + " " + self.creer_a + ")"
        return "(" + self.montant + " " + self.creer_a + ")"

