from flask import jsonify
from flask import request

from models import db
from services.user_service import create_logic, update_logic, show_logic, all_user
from services.ExceptionService import ExceptionService
#from app import app

def all():
    """
All users
---
responses:
  200:
    description: Tous les utilisateurs
    content:
      application/json:
        example:
          data:
            - email: "nkusumichee1367@gmail.com"
              id: 6
              nom: "NKUSU"
              prenom: "Michée"
              post_nom: "Michée"
              picture: "https://lh3.googleusercontent.com/a/ACg8ocJi-eceMufk1AQrcwp8ZUQ87nJDEHHKEsMyxXc2xqwtOqtq0w=s96-c"
              roles:
                - "ROLE_USER"
"""

    try :
        data = all_user()
        return jsonify({"message": "Done", "data": data}), 200
    except ExceptionService as e:
        return jsonify({"error": e.args, "details": e.code}), e.code
    except Exception as e:
        return jsonify({"error": "Token invalide", "details": str(e)}), 401

def show(id):
    """
    Show geographical data for a province
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the province
    responses:
      200:
        description: Geographical data of the province
        examples:
          application/json:
            - email: "nkusumichee1367@gmail.com"
              id: 6
              nom: "NKUSU"
              prenom: "Michée"
              post_nom: "Michée"
              picture: "https://lh3.googleusercontent.com/a/ACg8ocJi-eceMufk1AQrcwp8ZUQ87nJDEHHKEsMyxXc2xqwtOqtq0w=s96-c"
              roles:
                - "ROLE_USER"
    """
    data, code = show_logic(id)
    return jsonify(data), code

def update(id,data):
    resp, code = update_logic(id, data)
    return jsonify(resp), code


