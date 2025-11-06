# controllers/KPIController.py
from flask import request, jsonify
from services.kpis import (
    count_vehicle_by_camera,
    count_vehicule_by_transaction_and_type,
    count_vehicule_by_transaction_and_post,
    count_vehicule_by_transaction_and_road,
    count_vehicule_by_transaction_and_agent,
    revenues_by_vehicle_type,
    revenues_by_post,
    revenues_by_road,
    revenues_by_agent,
    visualization_transations,
    visualization_transations_by_vehicle_type,
    visualization_transations_by_post,
    visualization_transations_by_road,
    visualization_transations_by_agent,
    diff_between_revenue_collect_and_record_by_vehicle_type,
    diff_between_revenue_collect_and_record_by_post,
    diff_between_revenue_collect_and_record_by_road,
    diff_between_revenue_collect_and_record_by_agent
)


def _get_common_params():
    """
    Récupère les paramètres communs page, per_page, start_date et end_date depuis la requête.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    return page, per_page, start_date, end_date


# -------------------------
# KPI Vehicles
# -------------------------

def get_vehicle_count_by_camera():
    """
    Retourne le nombre de véhicules détectés par caméra.
    ---
    tags:
      - Vehicles
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Liste des véhicules par caméra
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = count_vehicle_by_camera(page, per_page, start_date, end_date)
    return jsonify(data)


def get_vehicle_count_by_type():
    """
    Retourne le nombre de véhicules par type.
    ---
    tags:
      - Vehicles
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Nombre de véhicules par type
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = count_vehicule_by_transaction_and_type(page, per_page, start_date, end_date)
    return jsonify(data)


def get_vehicle_count_by_post():
    """
    Retourne le nombre de véhicules par poste.
    ---
    tags:
      - Vehicles
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Nombre de véhicules par poste
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = count_vehicule_by_transaction_and_post(page, per_page, start_date, end_date)
    return jsonify(data)


def get_vehicle_count_by_road():
    """
    Retourne le nombre de véhicules par route.
    ---
    tags:
      - Vehicles
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Nombre de véhicules par route
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = count_vehicule_by_transaction_and_road(page, per_page, start_date, end_date)
    return jsonify(data)


def get_vehicle_count_by_agent():
    """
    Retourne le nombre de véhicules par agent.
    ---
    tags:
      - Vehicles
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Nombre de véhicules par agent
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = count_vehicule_by_transaction_and_agent(page, per_page, start_date, end_date)
    return jsonify(data)


# -------------------------
# KPI Revenues
# -------------------------

def get_revenues_by_vehicle_type():
    """
    Retourne les revenus par type de véhicule.
    ---
    tags:
      - Revenues
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Revenus par type de véhicule
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = revenues_by_vehicle_type(page, per_page, start_date, end_date)
    return jsonify(data)


def get_revenues_by_post():
    """
    Retourne les revenus par poste.
    ---
    tags:
      - Revenues
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Revenus par poste
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = revenues_by_post(page, per_page, start_date, end_date)
    return jsonify(data)


def get_revenues_by_road():
    """
    Retourne les revenus par route.
    ---
    tags:
      - Revenues
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Revenus par route
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = revenues_by_road(page, per_page, start_date, end_date)
    return jsonify(data)


def get_revenues_by_agent():
    """
    Retourne les revenus par agent.
    ---
    tags:
      - Revenues
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Revenus par agent
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = revenues_by_agent(page, per_page, start_date, end_date)
    return jsonify(data)


# -------------------------
# Visualizations
# -------------------------

def get_visualization_transactions():
    """
    Visualisation des transactions.
    ---
    tags:
      - Visualization
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Visualisation des transactions
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = visualization_transations(page, per_page, start_date, end_date)
    return jsonify(data)


def get_visualization_transactions_by_vehicle_type():
    """
    Visualisation des transactions par type de véhicule.
    ---
    tags:
      - Visualization
    parameters:
      - name: vehicle_type_id
        in: query
        type: integer
        required: true
        description: ID type de vehicule
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Visualisation des transactions par type de véhicule
    """
    page, per_page, start_date, end_date = _get_common_params()
    vehicle_type_id = request.args.get("vehicle_type_id", None, type=int)
    data = visualization_transations_by_vehicle_type(vehicle_type_id, page, per_page, start_date, end_date)
    return jsonify(data)


def get_visualization_transactions_by_post():
    """
    Visualisation des transactions par poste.
    ---
    tags:
      - Visualization
    parameters:
      - name: poste_id
        in: query
        type: integer
        required: true
        description: ID type de poste de peage
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Visualisation des transactions par poste
    """
    page, per_page, start_date, end_date = _get_common_params()
    poste_id = request.args.get("poste_id", None, type=int)
    data = visualization_transations_by_post(poste_id, page, per_page, start_date, end_date)
    return jsonify(data)


def get_visualization_transactions_by_road():
    """
    Visualisation des transactions par route.
    ---
    tags:
      - Visualization
    parameters:
      - name: route_id
        in: query
        type: integer
        required: true
        description: ID type de la route
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Visualisation des transactions par route
    """
    page, per_page, start_date, end_date = _get_common_params()
    route_id = request.args.get("route_id", None, type=int)
    data = visualization_transations_by_road(route_id, page, per_page, start_date, end_date)
    return jsonify(data)


def get_visualization_transactions_by_agent():
    """
    Visualisation des transactions par agent.
    ---
    tags:
      - Visualization
    parameters:
      - name: agent_id
        in: query
        type: integer
        required: true
        description: ID type de l'agent
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Visualisation des transactions par agent
    """
    page, per_page, start_date, end_date = _get_common_params()
    agent_id = request.args.get("agent_id", None, type=int)
    data = visualization_transations_by_agent(agent_id, page, per_page, start_date, end_date)
    return jsonify(data)


# -------------------------
# Différence revenus collectés vs enregistrés
# -------------------------

def get_diff_revenue_by_vehicle_type():
    """
    Différence entre revenus collectés et enregistrés par type de véhicule.
    ---
    tags:
      - Revenue Diff
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Différence revenus collectés vs enregistrés par type de véhicule
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = diff_between_revenue_collect_and_record_by_vehicle_type(page, per_page, start_date, end_date)
    return jsonify(data)


def get_diff_revenue_by_post():
    """
    Différence entre revenus collectés et enregistrés par poste.
    ---
    tags:
      - Revenue Diff
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Différence revenus collectés vs enregistrés par poste
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = diff_between_revenue_collect_and_record_by_post(page, per_page, start_date, end_date)
    return jsonify(data)


def get_diff_revenue_by_road():
    """
    Différence entre revenus collectés et enregistrés par route.
    ---
    tags:
      - Revenue Diff
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Différence revenus collectés vs enregistrés par route
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = diff_between_revenue_collect_and_record_by_road(page, per_page, start_date, end_date)
    return jsonify(data)


def get_diff_revenue_by_agent():
    """
    Différence entre revenus collectés et enregistrés par agent.
    ---
    tags:
      - Revenue Diff
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: start_date
        in: query
        type: string
      - name: end_date
        in: query
        type: string
    responses:
      200:
        description: Différence revenus collectés vs enregistrés par agent
    """
    page, per_page, start_date, end_date = _get_common_params()
    data = diff_between_revenue_collect_and_record_by_agent(page, per_page, start_date, end_date)
    return jsonify(data)
