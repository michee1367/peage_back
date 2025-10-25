#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()
from models import db
from geoalchemy2.types import Geometry
#from models.MetaRecord import MetaRecord
from datetime import datetime, timezone

from sqlalchemy.dialects import postgresql

# Creating the Inserttable for inserting data into the database


class User(db.Model):
    '''table des utilisateurs.'''

    __tablename__ = 'utilisateur'
    postgresql.JSON
    __fillables__ = ["nom", "post_nom","picture","prenom","email","phone"]
    __showables__= ["nom", "post_nom", "picture", "prenom", "email", "phone"]
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uniq_key = db.Column("uniq_key",db.String(80), nullable=True) # nom
    nom = db.Column("nom",db.String(80), nullable=True) # nom
    post_nom = db.Column("post_nom",db.String(80), nullable=True) # nom
    picture = db.Column("picture",db.String(255), nullable=True) # nom
    prenom = db.Column("prenom",db.String(80), nullable=True) # nom
    email = db.Column("email",db.String(80), nullable=False) # nom
    phone = db.Column("phone",db.String(80), nullable=True) # nom
    
    roles = db.Column("roles",postgresql.ARRAY(db.String(80)), nullable=True) # nom
    other_data = db.Column("other_data",postgresql.JSON) # other property
    
    activate_at = db.Column("activate_at",db.DateTime, nullable=True)
    deactivate_at = db.Column("deactivate_at",db.DateTime, nullable=True)
    
    
    created_at = db.Column("created_at",db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    deleted_at = db.Column("deleted_at",db.DateTime, nullable=True)
    # Méthode pour convertir le modèle en dictionnaire
    quarts = db.relationship("QuartDeTravail", back_populates="utilisateur")
    fichiers = db.relationship("FichierReglement", back_populates="utilisateur")
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getRoles(self) :
        if self.roles is None :
            return ["ROLE_VISITOR"]
        return self.roles
    
    def get_full_name(self) :
        return self.nom + " " + self.post_nom + " " + self.prenom
    def getWording(self) :
        return self.get_full_name()
    
    def setUniqKey(self) :
        pg_id = ""
        if self.nom :
            pg_id = pg_id + "-" + str(self.nom)
        if self.prenom :
            pg_id = pg_id + "-" + str(self.prenom)
        if self.post_nom :
            pg_id = pg_id + "-" + str(self.post_nom)
            
        self.uniq_key = pg_id
    # method used to represent a class's objects as a string
    def __repr__(self):
        return '<users %r>' % self.email
    
