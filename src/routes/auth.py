from flask import Blueprint
from controllers.authController import google_auth, logout, get_user, get_roles
from services.auth_service import auth_required
from hashlib import pbkdf2_hmac

auth = Blueprint('auth', __name__)

auth.route("/auth/google", methods=["POST"])(google_auth)
auth.route("/auth/logout", methods=["POST"])(logout)
auth.route("/auth/roles", methods=["GET"])(get_roles)

@auth.route("/auth/me", methods=["GET"])
@auth_required  # Appliquer le décorateur @me.auth pour protéger la route
def showUser():
    return get_user()