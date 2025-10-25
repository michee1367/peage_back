# models.py
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint

db = SQLAlchemy()

# ------------------------
# Poste de péage
# ------------------------
class PosteDePeage(db.Model):
    __tablename__ = "postes_de_peage"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    localisation = db.Column(db.String(512))
    date_creation = db.Column(DateTime, default=func.now())

    voies = db.relationship("Voie", back_populates="poste", cascade="all, delete-orphan")

# ------------------------
# Voie
# ------------------------
class Voie(db.Model):
    __tablename__ = "voies"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50))
    active = db.Column(Boolean, default=True)

    poste_id = db.Column(db.Integer, db.ForeignKey("postes_de_peage.id"), nullable=False)
    poste = db.relationship("PosteDePeage", back_populates="voies")

    equipements = db.relationship("Equipement", back_populates="voie", cascade="all, delete-orphan")
    quarts = db.relationship("QuartDeTravail", back_populates="voie", cascade="all, delete-orphan")

# ------------------------
# Equipement
# ------------------------
class Equipement(db.Model):
    __tablename__ = "equipements"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))                # ex: "POS", "Caméra", "Barrière"
    numero_serie = db.Column(db.String(255), unique=True)
    statut = db.Column(db.String(50))
    derniere_communication = db.Column(DateTime)

    voie_id = db.Column(db.Integer, db.ForeignKey("voies.id"), nullable=False)
    voie = db.relationship("Voie", back_populates="equipements")

# ------------------------
# CategorieVehicule
# ------------------------
class CategorieVehicule(db.Model):
    __tablename__ = "categories_vehicules"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    regle = db.Column(JSONB)   # JSON décrivant la règle (ex: {"essieux":2, "poids_max":3500})

    tarifs = db.relationship("Tarif", back_populates="categorie", cascade="all, delete-orphan")

# ------------------------
# Tarif
# ------------------------
class Tarif(db.Model):
    __tablename__ = "tarifs"

    id = db.Column(db.Integer, primary_key=True)
    devise = db.Column(db.String(10), nullable=False)
    montant = db.Column(Numeric(14, 2), nullable=False)
    date_debut_validite = db.Column(Date)
    date_fin_validite = db.Column(Date)

    categorie_id = db.Column(db.Integer, db.ForeignKey("categories_vehicules.id"), nullable=False)
    categorie = db.relationship("CategorieVehicule", back_populates="tarifs")

# ------------------------
# Caissier
# ------------------------
class Caissier(db.Model):
    __tablename__ = "caissiers"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    identifiant = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(50), default="caissier")

    quarts = db.relationship("QuartDeTravail", back_populates="caissier")

# ------------------------
# QuartDeTravail
# ------------------------
class QuartDeTravail(db.Model):
    __tablename__ = "quarts_de_travail"

    id = db.Column(db.Integer, primary_key=True)
    heure_ouverture = db.Column(DateTime, default=func.now())
    heure_fermeture = db.Column(DateTime)
    fond_ouverture = db.Column(Numeric(14,2), default=0)
    montant_cloture = db.Column(Numeric(14,2))

    voie_id = db.Column(db.Integer, db.ForeignKey("voies.id"), nullable=False)
    voie = db.relationship("Voie", back_populates="quarts")

    caissier_id = db.Column(db.Integer, db.ForeignKey("caissiers.id"), nullable=False)
    caissier = db.relationship("Caissier", back_populates="quarts")

    transactions = db.relationship("Transaction", back_populates="quart", cascade="all, delete-orphan")

# ------------------------
# Transaction (UUID)
# ------------------------
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    montant = db.Column(Numeric(14,2), nullable=False)
    devise = db.Column(db.String(10), nullable=False)
    moyen_paiement = db.Column(db.String(50))   # ex: "espece", "mobile_money", "carte"
    statut = db.Column(db.String(50), default="en_attente")  # en_attente, confirme, annule, echec
    plaque = db.Column(db.String(50))            # immatriculation, si disponible
    date_creation = db.Column(DateTime, default=func.now())
    date_confirmation = db.Column(DateTime)
    reference_externe = db.Column(db.String(255), index=True)  # ref fournie par prestataire externe (si existant)

    # Liens
    quart_id = db.Column(db.Integer, db.ForeignKey("quarts_de_travail.id"), nullable=True)
    quart = db.relationship("QuartDeTravail", back_populates="transactions")

    voie_id = db.Column(db.Integer, db.ForeignKey("voies.id"), nullable=False)
    voie = db.relationship("Voie")

    evenements = db.relationship("Evenement", back_populates="transaction", cascade="all, delete-orphan")

    # lien optionnel vers LigneReglement (reconciliation)
    ligne_reglement = db.relationship("LigneReglement", back_populates="transaction", uselist=False)

# ------------------------
# Evenement (UUID) -> journal immuable
# ------------------------
class Evenement(db.Model):
    __tablename__ = "evenements"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.String(100), nullable=False)   # ex: "paiement.initie", "barriere.ouverte"
    donnees = db.Column(JSONB)
    date_creation = db.Column(DateTime, default=func.now())
    hash_precedent = db.Column(db.String(128))
    hash_actuel = db.Column(db.String(128))

    transaction_id = db.Column(UUID(as_uuid=True), db.ForeignKey("transactions.id"), nullable=True)
    transaction = db.relationship("Transaction", back_populates="evenements")

# ------------------------
# FichierReglement
# ------------------------
class FichierReglement(db.Model):
    __tablename__ = "fichiers_reglement"

    id = db.Column(db.Integer, primary_key=True)
    fournisseur = db.Column(db.String(255), nullable=False)   # ex: "Airtel Money"
    date_fichier = db.Column(Date, nullable=False)
    montant_total = db.Column(Numeric(14,2), default=0)
    nombre_lignes = db.Column(db.Integer, default=0)
    # on peut stocker le fichier brut si besoin: fichier_blob = db.Column(db.LargeBinary)

    lignes = db.relationship("LigneReglement", back_populates="fichier", cascade="all, delete-orphan")

# ------------------------
# LigneReglement (reconciliation)
# ------------------------
class LigneReglement(db.Model):
    __tablename__ = "lignes_reglement"

    id = db.Column(db.Integer, primary_key=True)
    reference_externe = db.Column(db.String(255), nullable=False, index=True)
    montant = db.Column(Numeric(14,2), nullable=False)
    statut = db.Column(db.String(50))   # ex: "SUCCESS", "FAILED", "PENDING"
    transaction_id = db.Column(UUID(as_uuid=True), db.ForeignKey("transactions.id"), nullable=True)

    # relation vers transaction
    transaction = db.relationship("Transaction", back_populates="ligne_reglement")

    # relation vers fichier
    fichier_id = db.Column(db.Integer, db.ForeignKey("fichiers_reglement.id"), nullable=False)
    fichier = db.relationship("FichierReglement", back_populates="lignes")

    __table_args__ = (
        UniqueConstraint("fichier_id", "reference_externe", name="uq_fichier_reference"),
    )

# ------------------------
# (Option) Table vehicules pour référencer tags RFID, etc.
# ------------------------
class Vehicule(db.Model):
    __tablename__ = "vehicules"

    id = db.Column(db.Integer, primary_key=True)
    immatriculation = db.Column(db.String(50), index=True)
    tag_rfid = db.Column(db.String(255), unique=True)
    type_identification = db.Column(db.String(50))   # ex: "LAPI", "RFID", "MANUEL"
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories_vehicules.id"))
    proprietaire = db.Column(db.String(255))

    categorie = db.relationship("CategorieVehicule")
    # Si tu veux lier la transaction au véhicule, ajoute transaction.vehicule_id
