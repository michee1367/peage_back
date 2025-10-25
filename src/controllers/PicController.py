import json
from flask import jsonify
#, db
from services.picture import change_picture_record, get_dirname, path_rel_to_url, get_default_dirname
from services.ExceptionService import ExceptionService
from flask import request
import shutil
from werkzeug.utils import secure_filename

from flask import Flask, send_from_directory, abort
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def change_pic(enregistrement_id, table_name):
  """
Permet de changer la photo liée à un enregistrement.

---
tags:
  - Pics
consumes:
  - multipart/form-data
parameters:
  - name: enregistrement_id
    in: path
    type: integer
    required: true
    description: ID de l'enregistrement
  - name: table_name
    in: path
    type: string
    required: true
    description: Nom de la table
  - name: Authorization
    in: header
    type: string
    required: true
    description: Token d'authentification Bearer. Par exemple, "Bearer <votre_token>"
  - name: file
    in: formData
    type: file
    required: true
    description: Fichier image à uploader

responses:
  200:
    description: Photo mise à jour avec succès
    schema:
      type: object
      properties:
        message:
          type: string
          example: Settings updated successfully
  400:
    description: Requête invalide (valeurs incorrectes)
  404:
    description: Enregistrement non trouvé
  500:
    description: Erreur interne du serveur
"""
  try:
      file = request.files.get('file')

      if not file:
          return jsonify({"message": "Aucun fichier envoyé"}), 400

      if not allowed_file(file.filename):
          return jsonify({"message": "Format de fichier non autorisé. Formats acceptés : png, jpg, jpeg, gif"}), 400

      filename = secure_filename(file.filename)
      path_rel = change_picture_record(table_name, enregistrement_id, file)

      return jsonify({"message": "Photo mise à jour avec succès", "url": path_rel_to_url(path_rel)}), 201

  except Exception as e:
      return jsonify({"message": str(e)}), 500
    
    
def get_pic(filename, table_name) :
    """
    Récupère une photo à partir de son nom de fichier.
    ---
    tags:
      - Pics
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Nom du fichier image à récupérer
      - name: table_name
        in: path
        type: string
        required: true
        description: Nom de la tableme
    responses:
      200:
        description: Image retournée avec succès
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Fichier non trouvé
    """
    try:
        DOSSIER_PHOTOS=get_dirname(table_name)
        
        return send_from_directory(DOSSIER_PHOTOS, filename)
    except FileNotFoundError:
        abort(404, description="Fichier non trouvé")
    try:
        data = get_lang_possible()
        return jsonify(data), 200
        
    except Exception as e:
        # fallback pour toute autre exception
        return jsonify({"message": str(e)}), 500



def get_defalt_pic() :
    """
    Récupère la photo par defaut à partir de son nom de fichier.
    ---
    tags:
      - Pics
    responses:
      200:
        description: Image retournée avec succès
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Fichier non trouvé
    """
    try:
        DOSSIER_PHOTOS=get_default_dirname()
        
        return send_from_directory(DOSSIER_PHOTOS, "default.png")
    except FileNotFoundError:
        abort(404, description="Fichier non trouvé")
    try:
        data = get_lang_possible()
        return jsonify(data), 200
        
    except Exception as e:
        # fallback pour toute autre exception
        return jsonify({"message": str(e)}), 500