# routes.kpi.py
from flask import Blueprint
from controllers.KPIController import (
    get_vehicle_count_by_camera,
    get_vehicle_count_by_type,
    get_vehicle_count_by_post,
    get_vehicle_count_by_road,
    get_vehicle_count_by_agent,
    get_revenues_by_vehicle_type,
    get_revenues_by_post,
    get_revenues_by_road,
    get_revenues_by_agent,
    get_visualization_transactions,
    get_visualization_transactions_by_vehicle_type,
    get_visualization_transactions_by_post,
    get_visualization_transactions_by_road,
    get_visualization_transactions_by_agent,
    get_diff_revenue_by_vehicle_type,
    get_diff_revenue_by_post,
    get_diff_revenue_by_road,
    get_diff_revenue_by_agent
)

kpi_route = Blueprint('kpi_route', __name__)

# -------------------------
# Exemple de routes simplifiées
# -------------------------
kpi_route.route("/vehicle_count_by_camera", methods=["GET"])(get_vehicle_count_by_camera)
kpi_route.route("/vehicle_count_by_type", methods=["GET"])(get_vehicle_count_by_type)
kpi_route.route("/vehicle_count_by_post", methods=["GET"])(get_vehicle_count_by_post)
kpi_route.route("/vehicle_count_by_road", methods=["GET"])(get_vehicle_count_by_road)
kpi_route.route("/vehicle_count_by_agent", methods=["GET"])(get_vehicle_count_by_agent)

kpi_route.route("/revenues_by_vehicle_type", methods=["GET"])(get_revenues_by_vehicle_type)
kpi_route.route("/revenues_by_post", methods=["GET"])(get_revenues_by_post)
kpi_route.route("/revenues_by_road", methods=["GET"])(get_revenues_by_road)
kpi_route.route("/revenues_by_agent", methods=["GET"])(get_revenues_by_agent)

kpi_route.route("/visualization_transactions", methods=["GET"])(get_visualization_transactions)
kpi_route.route("/visualization_transactions_by_vehicle_type", methods=["GET"])(get_visualization_transactions_by_vehicle_type)
kpi_route.route("/visualization_transactions_by_post", methods=["GET"])(get_visualization_transactions_by_post)
kpi_route.route("/visualization_transactions_by_road", methods=["GET"])(get_visualization_transactions_by_road)
kpi_route.route("/visualization_transactions_by_agent", methods=["GET"])(get_visualization_transactions_by_agent)

kpi_route.route("/diff_revenue_by_vehicle_type", methods=["GET"])(get_diff_revenue_by_vehicle_type)
kpi_route.route("/diff_revenue_by_post", methods=["GET"])(get_diff_revenue_by_post)
kpi_route.route("/diff_revenue_by_road", methods=["GET"])(get_diff_revenue_by_road)
kpi_route.route("/diff_revenue_by_agent", methods=["GET"])(get_diff_revenue_by_agent)
