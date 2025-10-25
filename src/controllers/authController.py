from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
import jwt
import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS
#from flask_session import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import wraps
from services.auth_service import create_jwt
from models.User import User
from models import db
from services.user_service import create_logic
from tools.role import get_all_roles
#from app import app
import jwt
import base64
import json

from flask import current_app
#@app.route("/auth/google", methods=["POST"])
def google_auth():
    """
    insert data to a table
---
parameters:
  - name: body
    in: body
    required: true
    description: "body of request (doit avoir l'attribut `token` qui contient le token renvoyer par google)"
    schema:
        type: object
        properties:
            token:
                type: string
                description: jwt de google auth
                example: "eyJ0eXAiO..."

responses:
  201:
    description: "Reçcois l'attribut `token` qui contient le token renvoyer par google et Retourne le JWT de l'application qui sera utilisé dans les requêtes (dans le header `Authorization: Bearer eyJ...`) ainsi que les infos de l'utilisateur."
    examples:
      application/json:
        message: "Authentification réussie"
        jwt_token: "eyJ0eXAiO..."
        user:
          id: 1
          email: "toto@example.com"
          nom: "toto"
          post_nom: "post_nom"
          prenom: "toto"
          roles: 
            - ROLE_USER
          picture: "https://pic.google.com/tUhfyeGjdd"
          other_data:
            id: "hhfhfhfhf"
"""

    data = request.json
    token = data.get("token")
    #{"message": "Authentification réussie", "user": user.to_dict(), "jwt_token": jwt_token}
    try:
        # Vérifier le token Google
        #user_info = id_token.verify_oauth2_token(token, requests.Request(), current_app.config["CLIENT_ID"])
        
        arrToken = token.split(".")
        user_info = None
        
        if len(arrToken) != 3 :
          return jsonify({"error": "Token invalide"}), 401
        
        
        try:
          #print(arrToken[1])
          payloadToken = arrToken[1]
          missing_padding = len(payloadToken) % 4
          if missing_padding:
              payloadToken += "=" * (4 - missing_padding)

          decoded_bytes = base64.b64decode(payloadToken)
          #print(arrToken[1])
          decoded_string = decoded_bytes.decode("utf-8")  # Conversion en texte
          user_info = json.loads(decoded_string)
          
        except Exception as e:
          print(str(e))
          return jsonify({"error": "Token invalide"}), 401
          
        
        #user_info = jwt.decode(token, options={"verify_signature": False})
        
        # Créer un JWT à partir des informations de l'utilisateur
        jwt_token = create_jwt(user_info)
        print(user_info)
        
        #exit(1)
        data = {
            "email":user_info["email"],
            "nom":user_info["family_name"] if "family_name" in user_info else None,
            "post_nom":user_info["name"] if "name" in user_info else None,
            "prenom":user_info["given_name"] if "given_name" in user_info else None,
            "picture":user_info["picture"] if "picture" in user_info else None,
            "other_data":user_info,
        }
        #return jsonify({"message": "Authentification réussie", "user": data})
        
        user = create_logic(data)
        
        if user is None :
            return jsonify({"message":"authentification echoué"})
            
        #user.to_dict()
        # Sauvegarder le JWT dans la session (cookie)
        session["jwt_token"] = jwt_token

        return jsonify({"message": "Authentification réussie", "user": user.to_dict(), "jwt_token": jwt_token})
    except Exception as e:
        return jsonify({"error": "Token invalide", "details": str(e)}), 401

#@app.route("/auth/logout", methods=["POST"])
def logout():
    session.pop("jwt_token", None)
    return jsonify({"message": "Déconnexion réussie"}), 200

#@app.route("/auth/me", methods=["GET"])
#@auth_required  # Appliquer le décorateur @me.auth pour protéger la route
def get_user():
    # L'utilisateur authentifié est maintenant disponible via request.user
    return jsonify({"user": request.user})

def get_roles():
    """
  All roles
  ---
  responses:
    200:
      description: Tous les roles possible des utilisateurs
      content:
        application/json:
          example:
            data:
                roles:
                  - "ROLE_USER"
                  - "ROLE_ADMIN"
                  - "ROLE_INVESTIGATOR"
                  - "ROLE_ROOT"
                  - "ROLE_INVESTIGATOR"
  """
    # L'utilisateur authentifié est maintenant disponible via request.user
    return jsonify({"data": get_all_roles()})


