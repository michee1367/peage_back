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
    transactions = db.relationship("Transaction", back_populates="categorie", cascade="all, delete-orphan")
    
    
    def getWording(self) :
        return self.nom


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


# ------------------------
# Evenement (UUID) -> journal immuable
# ------------------------
class Evenement(db.Model):
    __tablename__ = "evenements"
    __fillables__ = ["type", "donnees", "date_creation", "transaction_id"]
    __rel_showables__= ["transaction"]
    __showables__= ["type", "donnees", "date_creation"]

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.String(100), nullable=False)   # ex: "paiement.initie", "barriere.ouverte"
    donnees = db.Column(JSONB)
    date_creation = db.Column(DateTime, default=func.now())
    hash_precedent = db.Column(db.String(128))
    hash_actuel = db.Column(db.String(128))

    transaction_id = db.Column(UUID(as_uuid=True), db.ForeignKey("transactions.id"), nullable=True)
    transaction = db.relationship("Transaction", back_populates="evenements")
    
    
    def getWording(self) :
        return self.type 

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

    fichiers = db.relationship("FichierReglement", back_populates="fournisseur")
    
    def getWording(self) :
        return self.nom 


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
    devise_id = db.Column(db.Integer, db.ForeignKey("devises.id"), nullable=False)
    devise = db.relationship("Devise")
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



# ------------------------
# Poste de péage
# ------------------------

# ------------------------
# Poste de péage
# ------------------------
class PosteDePeage(db.Model):
    __tablename__ = "postes_de_peage"
    __fillables__ = ["nom", "localisation", "date_creation", "voie_id"]
    __showables__= ["nom", "localisation", "date_creation"]

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    localisation = db.Column(db.String(512))
    date_creation = db.Column(DateTime, default=func.now())
    
    
    voie_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    voie = db.relationship("Voie", back_populates="postes")

    quarts = db.relationship("QuartDeTravail", back_populates="poste", cascade="all, delete-orphan")
    equipements = db.relationship("Equipement", back_populates="poste", cascade="all, delete-orphan")
    
        
    def getWording(self) :
        return self.nom 


# ------------------------
# QuartDeTravail
# ------------------------
class QuartDeTravail(db.Model):
    __tablename__ = "quarts_de_travail"
    __rel_showables__= ["poste", "utilisateur", "versement"]
    __fillables__ = ["heure_ouverture", "heure_fermeture", "montant_cloture", "poste_id", "utilisateur_id"]
    __showables__= ["heure_ouverture", "heure_fermeture", "montant_cloture", "utilisateur_id"]

    id = db.Column(db.Integer, primary_key=True)
    heure_ouverture = db.Column(DateTime, default=func.now())
    heure_fermeture = db.Column(DateTime)
    fond_ouverture = db.Column(Numeric(14,2), default=0)
    montant_cloture = db.Column(Numeric(14,2))
    
    poste_id = db.Column(db.Integer, db.ForeignKey("postes_de_peage.id"), nullable=False)
    poste = db.relationship("PosteDePeage", back_populates="quarts")
    
    versement_id = db.Column(db.Integer, db.ForeignKey("versements.id"), nullable=False)
    versement = db.relationship("Versement", back_populates="quarts")
    
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    utilisateur = db.relationship("User", back_populates="quarts")

    transactions = db.relationship("Transaction", back_populates="quart", cascade="all, delete-orphan")
    
    
    def getWording(self) :
        if self.utilisateur :
            return self.utilisateur.getWording() + "(" + str(self.heure_ouverture) + ')'
        return str(self.id) + "(" + str(self.heure_ouverture) + ')'


# ------------------------
# Transaction (UUID)
# ------------------------
class Transaction(db.Model):
    __tablename__ = "transactions"
    __rel_showables__= ["quart", "voie"]
    __fillables__ = ["devise", "montant", "moyen_paiement", 
                     "statut", "plaque", "date_confirmation", 
                     "reference_externe", "voie_id", "quart_id"]
    __showables__= ["devise", "montant", "moyen_paiement", "statut", "plaque", "date_creation", "date_confirmation", "reference_externe"]

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
    
    

# ------------------------
# Route
# ------------------------
class Route(db.Model):
    __tablename__ = "routes"
    __fillables__ = ["denomination","code", "direction", "type_identification", "active", "poste_id"]
    __showables__= ["denomination","code", "direction", "type_identification", "active"]

    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50))
    active = db.Column(Boolean, default=True)

    postes = db.relationship("PosteDePeage", back_populates="route", cascade="all, delete-orphan")
    
    
    def getWording(self) :
        return self.denomination + "("+ self.code +")"
