from flask import jsonify
from flask import request
from models.User import User
from flask_jwt_extended import create_access_token
import jwt
import datetime
from flask import request, jsonify, session
from functools import wraps
#from app import app
from flask import current_app
import jwt


# Fonction pour créer un JWT à partir des informations de l'utilisateur
def create_jwt(user_info):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=365)  # Le token expire après 1 heure
    payload = {
        "sub": user_info["email"],  # Identifiant de l'utilisateur
        "name": user_info.get("name"),
        "iat": datetime.datetime.utcnow(),  # Date d'émission
        "exp": expiration  # Date d'expiration
    }
    token = jwt.encode(payload, current_app.config["CLIENT_ID"], algorithm="HS256")
    return token

# Fonction pour décoder le JWT et vérifier sa validité
def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, current_app.config["CLIENT_ID"], algorithms=["HS256"])
        #print(decoded_token)
        user = User.query.filter(User.email== decoded_token["sub"]).first()
        if user :
            return user, None
        return None, "User not found" 
    except jwt.ExpiredSignatureError as e:
        return None, "Token expiré"
    except jwt.InvalidTokenError as e:
        #print(e)
        return None, "Token invalide"

# Définir un décorateur pour vérifier l'authentification via JWT
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifier si un JWT est présent dans la session (pour le frontend web)
        jwt_token = session.get("jwt_token")
        
        # Si la session ne contient pas de JWT, vérifier dans les en-têtes (pour l'application mobile)
        if not jwt_token:
            auth_header = request.headers.get("Authorization")
            if auth_header:
                # Le token est dans le format "Bearer <token>"
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == "bearer":
                    jwt_token = parts[1]

        if jwt_token:
            # Décoder le JWT et vérifier la validité
            decoded_token, error = decode_jwt(jwt_token)
            if decoded_token:
                # Ajouter l'utilisateur décodé à l'objet de la requête pour y accéder facilement dans la route
                request.user = decoded_token
                return f(*args, **kwargs)
            else:
                return jsonify({"error": error}), 401
        else:
            return jsonify({"error": "Non authentifié"}), 401

    return decorated_function

