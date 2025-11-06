import json
from models import db
from jsonschema import validate, exceptions
from services.ExceptionService import ExceptionService
#from services.unit import get_quantities, transform_quantity_data, transform_show, getSettingsWithoutUser, transform_record
#from models.Enregistrement import Enregistrement
from sqlalchemy.inspection import inspect
from datetime import datetime, timezone
import geopandas as gpd
import pandas as pd
from shapely import wkt 
#from models.TaskImport import CSV_IMPORT_TASK, EXCEL_IMPORT_TASK, ZIP_IMPORT_TASK, JSON_IMPORT_TASK, GEOJSON_IMPORT_TASK
import shutil
import os
from flask import current_app
from sqlalchemy import func
from shapely import wkt
import math
import numbers
from sqlalchemy import or_, and_, case
from tools.geo import wtkToJson
from services.picture import get_pic_url
#from models.EntityAdministration.territory import Territory
from tools.objects.PaginateReturn import PaginateReturn
from tools.model import get_attr_by_path
from models.Vehicule import Vehicule
from models.Transaction import Transaction
from models.CategorieVehicule import CategorieVehicule
from models.QuartDeTravail import QuartDeTravail
from models.PosteDePeage import PosteDePeage
from models.Route import Route
from models.User import User
from models.Devise import Devise
from models.LigneReglement import LigneReglement
from models.Versement import Versement
from models.Collecte import Collecte
from tools.date import parse_date
from services.models import record_to_dict


# -------------------------
# Fonction privée
# -------------------------


# -------------------------
# FONCTION GÉNÉRIQUE D'AJOUT DE FILTRE DE DATE
# -------------------------
def add_interval_in_query(model, field_name, query, start_date=None, end_date=None):
    field = getattr(model, field_name, None)
    if field is None:
        raise AttributeError(f"Le champ '{field_name}' n'existe pas dans le modèle {model.__name__}.")

    if not start_date and not end_date:
        return query
    if start_date and not end_date:
        return query.filter(field >= start_date)
    if not start_date and end_date:
        return query.filter(field < end_date)
    return query.filter(field.between(start_date, end_date))



# ------------------
# Consultation en temps réel du trafic et des recettes par type de véhicule, poste, route, period, agent
# ------------------

# Nombre des vehicules identifié par camera

def count_vehicle_by_camera(page=1, per_page=10, start_date=None, end_date=None) :
    return {
        "data":[],
        "pagination": {
                "page": page,
                "per_page": per_page,
                "total": 0,
                "pages": 0,
                "has_next": False,
                "has_prev": False
            }
    }
from sqlalchemy import func
from datetime import datetime

# -------------------------
# NOMBRE DE VÉHICULES PAR TYPE
# -------------------------
def count_vehicule_by_transaction_and_type(page=1, per_page=10, start_date=None, end_date=None):
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            CategorieVehicule.id.label("categorie_vehicule_id"),
            CategorieVehicule.nom.label("categorie_vehicule_nom"),
            func.count(Transaction.id).label("total_transaction"),
            func.count(func.distinct(Transaction.plaque)).label("total_vehicle")
        )
        .join(CategorieVehicule, CategorieVehicule.id == Transaction.categorie_id)
    )

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(CategorieVehicule.id, CategorieVehicule.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "categorie_vehicule_id": r.categorie_vehicule_id,
            "categorie_vehicule_nom": r.categorie_vehicule_nom,
            "total_transaction": int(r.total_transaction or 0),
            "total_vehicle": int(r.total_vehicle or 0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)


# -------------------------
# NOMBRE DE VÉHICULES PAR POSTE DE PÉAGE
# -------------------------
def count_vehicule_by_transaction_and_post(page=1, per_page=10, start_date=None, end_date=None):
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            PosteDePeage.id.label("poste_de_peage_id"),
            PosteDePeage.nom.label("poste_de_peage_nom"),
            func.count(Transaction.id).label("total_transaction"),
            func.count(func.distinct(Transaction.plaque)).label("total_vehicle")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
    )

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(PosteDePeage.id, PosteDePeage.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "poste_de_peage_id": r.poste_de_peage_id,
            "poste_de_peage_nom": r.poste_de_peage_nom,
            "total_transaction": int(r.total_transaction or 0),
            "total_vehicle": int(r.total_vehicle or 0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)


# -------------------------
# NOMBRE DE VÉHICULES PAR ROUTE
# -------------------------
def count_vehicule_by_transaction_and_road(page=1, per_page=10, start_date=None, end_date=None):
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            Route.id.label("route_id"),
            Route.denomination.label("route_nom"),
            func.count(Transaction.id).label("total_transaction"),
            func.count(func.distinct(Transaction.plaque)).label("total_vehicle")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
        .join(Route, Route.id == PosteDePeage.route_id)
    )

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(Route.id, Route.denomination)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "route_id": r.route_id,
            "route_nom": r.route_nom,
            "total_transaction": int(r.total_transaction or 0),
            "total_vehicle": int(r.total_vehicle or 0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)


# -------------------------
# NOMBRE DE VÉHICULES PAR AGENT
# -------------------------
def count_vehicule_by_transaction_and_agent(page=1, per_page=10, start_date=None, end_date=None):
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            User.id.label("utilisateur_id"),
            User.nom.label("utilisateur_nom"),
            func.count(Transaction.id).label("total_transaction"),
            func.count(func.distinct(Transaction.plaque)).label("total_vehicle")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(User, User.id == QuartDeTravail.utilisateur_id)
    )

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(User.id, User.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "utilisateur_id": r.utilisateur_id,
            "utilisateur_nom": r.utilisateur_nom,
            "total_transaction": int(r.total_transaction or 0),
            "total_vehicle": int(r.total_vehicle or 0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)



# Recettes 

def revenues_by_vehicle_type(page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            CategorieVehicule.id.label("categorie_vehicule_id"),
            CategorieVehicule.nom.label("categorie_vehicule_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transaction")
        )
        .join(CategorieVehicule, CategorieVehicule.id == Transaction.categorie_id)
        .join(Devise, Devise.id == Transaction.devise_id)
    )
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(CategorieVehicule.id, CategorieVehicule.nom, Devise.id, Devise.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "categorie_vehicule_id": r.categorie_vehicule_id,
            "categorie_vehicule_nom": r.categorie_vehicule_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transaction": float(r.total_transaction or 0.0),
            "total_vehicle": float(r.total_vehicle or 0.0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass

def revenues_by_post(page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            PosteDePeage.id.label("poste_peage_id"),
            PosteDePeage.nom.label("poste_peage_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transaction")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
        .join(Devise, Devise.id == Transaction.devise_id)
    )
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(PosteDePeage.id, PosteDePeage.nom, Devise.id, Devise.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "poste_peage_id": r.poste_peage_id,
            "poste_peage_nom": r.poste_peage_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transaction": float(r.total_transaction or 0.0),
            "total_vehicle": float(r.total_vehicle or 0.0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass

def revenues_by_road(page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            Route.id.label("route_id"),
            Route.denomination.label("route_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transaction")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
        .join(Route, Route.id == PosteDePeage.route_id)
        .join(Devise, Devise.id == Transaction.devise_id)
    )
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(Route.id, Route.denomination, Devise.id, Devise.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "route_id": r.route_id,
            "route_nom": r.route_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transaction": float(r.total_transaction or 0.0),
            "total_vehicle": float(r.total_vehicle or 0.0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass

def revenues_by_agent(page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = (
        db.session.query(
            User.id.label("utilisateur_id"),
            User.nom.label("utilisateur_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transaction")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(User, User.id == QuartDeTravail.utilisateur_id)
        .join(Devise, Devise.id == Transaction.devise_id)
    )
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    query = query.group_by(User.id, User.nom, Devise.id, Devise.nom)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "utilisateur_id": r.utilisateur_id,
            "utilisateur_nom": r.utilisateur_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transaction": float(r.total_transaction or 0.0),
            "total_vehicle": float(r.total_vehicle or 0.0)
        }
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass


# ------------------
# Visualisation des opérations par date, poste et agent.
# ------------------

def visualization_transations(page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = Transaction.query()
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        record_to_dict(r)
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass


def visualization_transations_by_vehicle_type(vehicle_type_id,page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = Transaction.query\
            .filter(CategorieVehicule.id == vehicle_type_id)\
            .join(CategorieVehicule, CategorieVehicule.id == Transaction.categorie_id)
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        record_to_dict(r)
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)

def visualization_transations_by_post(post_id, page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = Transaction.query\
            .filter(PosteDePeage.id == post_id)\
            .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)\
            .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        record_to_dict(r)
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass

def visualization_transations_by_road(road_id, page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = Transaction.query\
            .filter(Route.id == road_id)\
            .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)\
            .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)\
            .join(Route, Route.id == PosteDePeage.route_id)
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        record_to_dict(r)
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass

def visualization_transations_by_agent(agent_id, page=1, per_page=10, start_date=None, end_date=None) :
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    query = Transaction.query\
            .filter(User.id == agent_id)\
            .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)\
            .join(User, User.id == QuartDeTravail.utilisateur_id)
    

    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        record_to_dict(r)
        for r in pagination.items
    ]

    return _format_paginated_result(pagination, result)
    pass

# Propriétés principale

# ------------------
# Vérification automatique entre les montants collectés et les enregistrements transmis par poste, route, periode, agent
# ------------------

def diff_between_revenue_collect_and_record_by_vehicle_type(page=1, per_page=10, start_date=None, end_date=None) :
    """
    Compare le total des transactions et des transactions réglées
    par catégorie de véhicule, avec pagination et filtrage par intervalle de dates.
    """

    # --- Validation et conversion des dates ---
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    # --- Construction de la requête ---
    query = (
        db.session.query(
            CategorieVehicule.id.label("categorie_vehicule_id"),
            CategorieVehicule.nom.label("categorie_vehicule_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transactions"),
            func.sum(
                case(
                    (LigneReglement.id.isnot(None), Transaction.montant),
                    else_=0
                )
            ).label("transactions_reglees")
        )
        .join(CategorieVehicule, CategorieVehicule.id == Transaction.categorie_id)
        .join(Devise, Devise.id == Transaction.devise_id)
        .outerjoin(LigneReglement, LigneReglement.transaction_id == Transaction.id)
    )

    # --- Application du filtre temporel ---
    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)

    # --- Groupement par catégorie ---
    query = query.group_by(CategorieVehicule.id, CategorieVehicule.nom, Devise.id, Devise.nom)

    # --- Pagination ---
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # --- Résultats formatés ---
    results = [
        {
            "categorie_vehicule_id": r.categorie_vehicule_id,
            "categorie_vehicule_nom": r.categorie_vehicule_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transactions": float(r.total_transactions or 0),
            "transactions_reglees": float(r.transactions_reglees or 0),
            "transactions_non_reglees": float((r.total_transactions or 0) - (r.transactions_reglees or 0))
        }
        for r in pagination.items
    ]

    # --- Formatage standard (avec totaux de pagination) ---
    return _format_paginated_result(pagination, results)
    pass

def diff_between_revenue_collect_and_record_by_post(page=1, per_page=10, start_date=None, end_date=None) :
    """
    Compare le total des transactions et des transactions vesées dans un poste par des agents,
    avec pagination et filtrage par intervalle de dates.
    """

    # Validation et conversion des dates
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    # Construction de la requête
    query = (
        db.session.query(
            PosteDePeage.id.label("poste_peage_id"),
            PosteDePeage.nom.label("poste_peage_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transactions"),
            func.sum(
                case(
                    (Versement.id.isnot(None), Versement.montant),
                    else_=0
                )
            ).label("transactions_versees")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
        .join(Devise, Devise.id == Transaction.devise_id)
        .outerjoin(Versement, Versement.quart_id == QuartDeTravail.id)
    )

    # Application du filtre de date si nécessaire
    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)

    # Groupement par agent
    query = query.group_by(PosteDePeage.id, PosteDePeage.nom, Devise.id, Devise.nom)

    # Application de la pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Format des résultats
    results = [
        {
            "poste_peage_id": r.poste_peage_id,
            "poste_peage_nom": r.poste_peage_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transactions": float(r.total_transactions or 0),
            "transactions_versees": float(r.transactions_versees or 0),
            "transactions_non_reglees": float((r.total_transactions or 0) - (r.transactions_versees or 0))
        }
        for r in pagination.items
    ]

    # Formatage standardisé
    return _format_paginated_result(pagination, results)
    pass


def diff_between_revenue_collect_and_record_by_road(page=1, per_page=10, start_date=None, end_date=None) :
    """
    Compare le total des transactions et des transactions collectées dans des postes d'une route par des agents,
    avec pagination et filtrage par intervalle de dates.
    """

    # Validation et conversion des dates
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    # Construction de la requête
    query = (
        db.session.query(
            Route.id.label("route_id"),
            Route.denomination.label("route_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transactions"),
            func.sum(
                case(
                    (Collecte.id.isnot(None), Collecte.montant),
                    else_=0
                )
            ).label("transactions_collectees")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(PosteDePeage, PosteDePeage.id == QuartDeTravail.poste_id)
        .join(Route, Route.id == PosteDePeage.route_id)
        .join(Devise, Devise.id == Transaction.devise_id)
        .outerjoin(Collecte, Collecte.poste_id == PosteDePeage.id)
    )

    # Application du filtre de date si nécessaire
    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)

    # Groupement par agent
    query = query.group_by(Route.id, Route.denomination, Devise.id, Devise.nom)

    # Application de la pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Format des résultats
    results = [
        {
            "route_id": r.route_id,
            "route_nom": r.route_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transactions": float(r.total_transactions or 0),
            "transactions_collectees": float(r.transactions_collectees or 0),
            "transactions_non_reglees": float((r.total_transactions or 0) - (r.transactions_collectees or 0))
        }
        for r in pagination.items
    ]

    # Formatage standardisé
    return _format_paginated_result(pagination, results)
    pass

def diff_between_revenue_collect_and_record_by_agent(page=1, per_page=10, start_date=None, end_date=None) :
    """
    Compare le total des transactions et des transactions réglées par agent,
    avec pagination et filtrage par intervalle de dates.
    """

    # Validation et conversion des dates
    start_datetime = parse_date(start_date)
    end_datetime = parse_date(end_date)

    if start_date and not start_datetime:
        raise ValueError("Le champ 'start_date' n'est pas une date valide.")
    if end_date and not end_datetime:
        raise ValueError("Le champ 'end_date' n'est pas une date valide.")

    # Construction de la requête
    query = (
        db.session.query(
            User.id.label("utilisateur_id"),
            User.nom.label("utilisateur_nom"),
            Devise.id.label("devise_id"),
            Devise.nom.label("devise_nom"),
            func.sum(Transaction.montant).label("total_transactions"),
            func.sum(
                case(
                    (LigneReglement.id.isnot(None), Transaction.montant),
                    else_=0
                )
            ).label("transactions_reglees")
        )
        .join(QuartDeTravail, QuartDeTravail.id == Transaction.quart_id)
        .join(User, User.id == QuartDeTravail.utilisateur_id)
        .join(Devise, Devise.id == Transaction.devise_id)
        .outerjoin(LigneReglement, LigneReglement.transaction_id == Transaction.id)
    )

    # Application du filtre de date si nécessaire
    query = add_interval_in_query(Transaction, "date_creation", query, start_datetime, end_datetime)

    # Groupement par agent
    query = query.group_by(User.id, User.nom, Devise.id, Devise.nom)

    # Application de la pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Format des résultats
    results = [
        {
            "utilisateur_id": r.utilisateur_id,
            "utilisateur_nom": r.utilisateur_nom,
            "devise_id": r.devise_id,
            "devise_nom": r.devise_nom,
            "total_transactions": float(r.total_transactions or 0),
            "transactions_reglees": float(r.transactions_reglees or 0),
            "transactions_non_reglees": float((r.total_transactions or 0) - (r.transactions_reglees or 0))
        }
        for r in pagination.items
    ]

    # Formatage standardisé
    return _format_paginated_result(pagination, results)
    pass


# ---------------------------------------
# Identification et signalement des anomalies.
# ---------------------------------------



# -------------------------
# FONCTION UTILITAIRE POUR FORMATER LES RÉSULTATS
# -------------------------
def _format_paginated_result(pagination, result):
    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
        "data": result
    }

