#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()
from models import db
from geoalchemy2.types import Geometry
from models.User import User
from datetime import datetime, timezone

from sqlalchemy.dialects import postgresql


# Creating the Inserttable for inserting data into the database


class Pic(db.Model):
    '''table des photo.'''

    __tablename__ = 'photo'
    #postgresql.JSON
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #unite = db.Column("unite",db.Float, nullable=False) # nom
    nom = db.Column("nom",db.String(255), nullable=False) # nom
    enregistrement_id = db.Column("enregistrement_id",db.String(255), nullable=False) # nom
    nom_table = db.Column("nom_table",db.String(255), nullable=False) # nom
    #props = db.Column(postgresql.JSON) # other property
    #other_data = db.Column("other_data",postgresql.JSON) # other property
    
    created_at = db.Column("created_at",db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column("updated_at",db.DateTime, nullable=True)
    # Méthode pour convertir le modèle en dictionnaire
    def to_dict(self):
        data_dict = {
            "id":self.id,
            "lang":self.nom,
            "nom_table":self.nom_table,
            #"id":self.id
        }
        return data_dict
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # method used to represent a class's objects as a string
    def __repr__(self):
        return '<unit %r>' % self.id
    
