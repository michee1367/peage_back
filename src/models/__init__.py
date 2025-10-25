import os, glob
from flask_sqlalchemy import SQLAlchemy
from tools.packages import alls

db = SQLAlchemy()

#__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
__all__ = alls(__file__)

#print(__all__)

#from models.MetaRecord import MetaRecord
#from models.Record import Record

from models.User import User
#from models.Agent import Agent
from models.Pic import Pic
#from models.Caissier import Caissier
from models.CategorieVehicule import CategorieVehicule
from models.Equipement import Equipement
from models.Evenement import Evenement
from models.FichierReglement import FichierReglement
from models.LigneReglement import LigneReglement
from models.PosteDePeage import PosteDePeage
from models.QuartDeTravail import QuartDeTravail
from models.Tarif import Tarif
from models.Transaction import Transaction
from models.Vehicule import Vehicule
from models.Voie import Voie
from models.Fournisseur import Fournisseur
from models.PassageVehicule import PassageVehicule

#from models.UserAgent import UserAgent
#from models.Office import Office
#from models.Visit import Visit
#from models.Visitor import Visitor
#from models.Enregistrement import Enregistrement


#from models.DrinkingWaterSupply.Fountain import Fountain
#from models.DrinkingWaterSupply.DistributionNetwork import DistributionNetwork


#from models.Education.EducationInstitution import EducationInstitution
#from models.Education.EducationInstitutionYear import EducationInstitutionYear
#from models.Education.InstitutionTypeEduction import InstitutionTypeEduction
#from models.Education.EducationInstitutionCategory import EducationInstitutionCategory


#from models.EntityAdministration.territoryYear import TerritoryYear
#from models.EntityAdministration.city import City
#from models.EntityAdministration.locality import Locality
#from models.EntityAdministration.pop import TerritoryPop
#from models.EntityAdministration.province import Province
#from models.EntityAdministration.etd import ETD
#from models.EntityAdministration.territory import Territory


#from models.ExistingPlants.powerPlant import PowerPlant
#from models.ExistingPlants.ownerAndOrOSER import OwnerAndOrOSER
#from models.ExistingPlants.powerPlantTerritoryHist import PowerPlantTerritoryHist
#from models.ExistingPlants.powerPlantTerritory import PowerPlantTerritory
#from models.ExistingPlants.substation import SubStation


#from models.ExistingPowerLines.powerLine import PowerLine
#from models.ExistingPowerLines.powerLineNature import  PowerLineNature
#from models.ExistingPowerLines.powerLineType import PowerLineType
#from models.ExistingPowerLines.TerritoryCross import TerritoryCross


#from models.Health.HealthInstitution import HealthInstitution
#from models.Health.HealthInstitutionYear import HealthInstitutionYear
#from models.Health.HealthInstitutionCategory import HealthInstitutionCategory
#from models.Health.HealthInstitutionService import HealthInstitutionService
#from models.Health.HealthZone import HealthZone
#from models.Health.HealthServiceOffered import HealthServiceOffered
#from models.Health.HealthZoneTerritory import HealthZoneTerritory


#from models.EnergicPotentials.EnergicPotential import EnergicPotential
#from models.EnergicPotentials.EnergicPotentialTerritory import EnergicPotentialTerritory

#from models.IndividualSets.IndividualSet import IndividualSet
#from models.IndividualSets.IndividualSetSupplier import IndividualSetSupplier
#from models.IndividualSets.IndividualSetTerritory import IndividualSetTerritory
#from models.IndividualSets.IndividualSetTerritoryHist import IndividualSetTerritoryHist

#from models.LocalEconomy.ConsumptionCenter import ConsumptionCenter
#from models.LocalEconomy.EconomicActivity import  EconomicActivity
#from models.LocalEconomy.EconomicActivityYear import  EconomicActivityYear
#from models.LocalEconomy.EconomicActivityType import   EconomicActivityType
#from models.LocalEconomy.ConsumptionCenterEconomicActivity import   ConsumptionCenterEconomicActivity
#from models.LocalEconomy.Equipment import   Equipment


#from models.MultiSectorData.FishingAreas import FishingAreas
#from models.MultiSectorData.FishingAreasYear import FishingAreasYear
#from models.MultiSectorData.ICCN import ICCN
#from models.MultiSectorData.ICCNYear import ICCNYear
#from models.MultiSectorData.Industry import Industry
#from models.MultiSectorData.IndustryYear import IndustryYear
#from models.MultiSectorData.MiningAreas import  MiningAreas
#from models.MultiSectorData.MiningAreasYear import  MiningAreasYear
#from models.MultiSectorData.PME import PME
#from models.MultiSectorData.PMEYear import PMEYear


#from models.PlacesOfWorship.PlaceOfWorship import PlaceOfWorship
#from models.PlacesOfWorship.PlaceOfWorshipYear import PlaceOfWorshipYear

#from models.Projects.Line import Line
#from models.Projects.ProgressStatus import ProgressStatus
#from models.Projects.Project import Project
#from models.Projects.ProjectComponent import ProjectComponent
#from models.Projects.Substations import Substations
#from models.Projects.Transformers import Transformers
#from models.Projects.DessertTerritoryProject import DessertTerritoryProject
#from models.Projects.DessertTerritoryProjectProgram import DessertTerritoryProjectProgram
#from models.Projects.ProjectProgram import ProjectProgram
#from models.Projects.ProjectDocument import ProjectDocument
#from models.Projects.ProjectLocality import ProjectLocality


#from models.SolarAndWindPotential.SolarPotential import SolarPotential
#from models.SolarAndWindPotential.SolarPotentialTerritory import SolarPotentialTerritory
#from models.SolarAndWindPotential.WindPotential import WindPotential
#from models.SolarAndWindPotential.WindPotentialLocality import WindPotentialLocality


#from models.Telecommunication.TelecommunicationNetworkAccessPoint import TelecommunicationNetworkAccessPoint
#from models.Telecommunication.TelecommunicationNetworkAccessPointYear import TelecommunicationNetworkAccessPointYear
#from models.Telecommunication.TelecommunicationOperator import TelecommunicationOperator
#from models.Telecommunication.MobileSubscriberBase import MobileSubscriberBase


#from models.WaysOfCommunication.WayOfCommunication import WaysOfCommunication
#rom models.WaysOfCommunication.ModeOfTransport import ModeOfTransport
#from models.WaysOfCommunication.RoadSurface import RoadSurface
#from models.WaysOfCommunication.ModeOfTransport import ModeOfTransport
#from models.WaysOfCommunication.SectionWay import SectionWay
#from models.WaysOfCommunication.WayOfCommTerritory import WayOfCommTerritory
#from models.WaysOfCommunication.WayOfCommModeOfTransport import WayOfCommModeOfTransport


#from models.TaskImport import TaskImport


#from models.Notification import Notification, UserNotification


#Sfrom models.Pic import Pic