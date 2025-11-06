import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
from datetime import datetime, timezone

# ------------------------
# Devise
# ------------------------
class Devise(db.Model):
    __tablename__ = "devises"
    __fillables__ = ["nom", "sign", ]
    __showables__= ["id", "nom", "sign"]
    __rel_showables__= []

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(10), nullable=False)
    sign = db.Column(db.String(10), nullable=False)
    
    creer_a = db.Column("created_at",db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    supprimer_a = db.Column("deleted_at",db.DateTime, nullable=True)
    
    
    def getWording(self) :
        return self.nom + "(" +self.sign+")"
