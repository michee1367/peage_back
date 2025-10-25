from flask import Blueprint
from controllers.userController import all, update, show
#from hashlib import pbkdf2_hmac
from flask import request

users = Blueprint('users', __name__)

users.route("/", methods=["GET"])(all)

@users.route("/<id>/update", methods=["POST"])
def updateUser(id):
    """
Update user data
---
parameters:
  - name: id
    in: path
    required: true
    description: ID of the user
    schema:
      type: integer
  - name: body
    in: body
    required: true
    description: Request body
    schema:
      type: object
      properties:
        nom:
          type: string
          description: Name of the user
        prenom:
          type: string
          description: Firstname of the user
        post_nom:
          type: string
          description: Lastname of the user
        email:
          type: string
          description: Email of the user
        roles:
          type: array
          description: Roles of the user
          items:
            type: string
      example:
        nom: "NKUSU"
        prenom: "Michée"
        post_nom: "Michée"
        email: "nkusumichee1367@gmail.com"
        picture: "https://lh3.googleusercontent.com/a/ACg8ocJi-eceMufk1AQrcwp8ZUQ87nJDEHHKEsMyxXc2xqwtOqtq0w=s96-c"
        roles:
          - "ROLE_USER"

responses:
  200:
    description: User data successfully updated
    content:
      application/json:
        example:
          message: "Data updated successfully"
"""
    return update(id, request.json)

@users.route('/<id>', methods=['GET'])
def showUser(id):
    """
    Show user
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
    return show(id)