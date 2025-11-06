import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Numeric, DateTime, Date, Boolean, func, UniqueConstraint
from models import db
# ------------------------
# Voie
# ------------------------
class Route(db.Model):
    __tablename__ = "routes"
    __fillables__ = ["denomination","code", "direction", "type_identification", "active"]
    __showables__= ["denomination","code", "direction", "type_identification", "active"]

    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50))
    active = db.Column(Boolean, default=True)

    postes = db.relationship("PosteDePeage", back_populates="route", cascade="all, delete-orphan")
    
    
    def getWording(self) :
        return self.denomination + "("+ self.code +")"
