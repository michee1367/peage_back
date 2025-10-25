import json
from flask import jsonify
from models import db
#, db
from services.models import get_models, save_data, get_schema,  update_data, get_all_records_file, \
  get_all_records_save, get_search_model, get_records_save #, insert_data, validate_data
  
#from services.compress.model import get_search_model_compress
#from services.data_tempo import validate_data
  
#from services.import_file import get_data_import
#from services.data_tempo import get_records
#from services.form_service import insert_data
from services.ExceptionService import ExceptionService
from flask import request
from sqlalchemy import text
from flask import current_app, send_file, after_this_request
import os
#from services.import_file import upload_file
import shutil
from flask import Response

#MetaRecordController
def getAllModels():
    """
    Show all models data
    ---
    responses:
      200:
        description: all data of the models
        examples:
          application/json: {
            "activite_economique": {
                "fields": {
                    "denomination": "VARCHAR(80)",
                    "geomCentroid": "geometry(POINT,4326)",
                    "production_actuelle": "FLOAT",
                    "production_potentielle": "FLOAT",
                    "territoire_id": "INTEGER",
                    "type_id": "INTEGER"
                },
                "relations": {
                    "territoire_id": "territoire_ville",
                    "type_id": "type_activite_economique"
                }
            }
        }
    """
    return jsonify(get_models())


def get_schema_by_table_name(table_name):
    """
    Show schema by tables
    ---
    parameters:
      - name: table_name
        in: path
        type: string
        required: true
        description: The name of the table
    responses:
        200:
            description: all data of the models
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            denomination:
                                type: string
                            geomCentroid:
                                type: string
                            production_actuelle:
                                type: number
                            production_potentielle:
                                type: number
                            territoire_id:
                                type: integer
                            type_id:
                                type: integer
                        required:
                            - denomination
                            - production_actuelle
                            - production_potentielle
                    examples:
                        application/json:
                            denomination: "Centrale Hydro"
                            geomCentroid: "POINT(30.5 -1.2)"
                            production_actuelle: 150.5
                            production_potentielle: 300.0
                            territoire_id: 3
                            type_id: 2
    """
    schema =  jsonify(get_schema(table_name))
    if not schema:
        return jsonify({"error": "Table not found"}), 404
    
    return schema


def insert_data_by_table_name(table_name):
    """
    insert data to a table
---
parameters:
  - name: body
    in: body
    required: true
    description: body of request
    schema:
      type: object
      properties:
        props:
          type: object
          description: properties of the metadata
          example:
            denomination: "Peche de poisson capitain"
            production_actuelle: 40000
            production_potentielle: 40000
  - name: table_name
    in: path
    type: string
    required: true
    description: The name of the table

responses:
  201:
    description: all data of the models
    content:
      application/json:
        examples:
          application/json:
            value:
              message: "Data inserted successfully"
    """
    data = request.json
    if "props" not in data :
        return jsonify({"message": "bad data format"}),400
    (resp, code) = save_data(table_name, data["props"])
    
    return jsonify(resp),code

def get_all_save_records_by_table_name(table_name):
    """
    Show all save records of a table
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Page number for pagination (default is 1)
      - name: per_page
        in: query
        type: integer
        required: false
        description: Number of records per page (default is 10)
      - name: is_short
        in: query
        type: boolean
        required: false
        description: Number of records per page (default is 10)
    responses:
        200:
          description: All save data of the model with pagination info
          examples:
            application/json: 
              {
                "data": [
                  {
                    "id": 1,
                    "denomination": "Peche de poisson capitain",
                    "geomCentroid": null,
                    "production_actuelle": 40000.0,
                    "production_potentielle": 40000.0,
                    "territoire_id": null,
                    "type_id": null
                  }
                ],
                "pagination": {
                  "page": 1,
                  "per_page": 10,
                  "total": 50,
                  "pages": 5,
                  "has_next": true,
                  "has_prev": false
                }
              }
"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    isShort = request.args.get('is_short', False)
    if isShort and  not (isShort == "false") :
      isShort=True
    else :
      isShort=False
      
    (resp, code) = get_all_records_save(table_name, page, per_page, isShort)
    
    return jsonify(resp),code


def get_save_records_by_table_name(table_name, record_id):
    """
    Show records of a table and id
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Page number for pagination (default is 1)
      - name: per_page
        in: query
        type: integer
        required: false
        description: Number of records per page (default is 10)
      - name: is_short
        in: query
        type: boolean
        required: false
        description: Number of records per page (default is 10)
    responses:
        200:
          description: All save data of the model with pagination info
          examples:
            application/json: 
              {
                "data": {
                    "id": 1,
                    "denomination": "Peche de poisson capitain",
                    "geomCentroid": null,
                    "production_actuelle": 40000.0,
                    "production_potentielle": 40000.0,
                    "territoire_id": null,
                    "type_id": null
                  }
              }
"""
      
    (resp, code) = get_records_save(table_name, record_id)
    
    return jsonify(resp),code


def get_all_records_by_table_name_download(table_name):
    """
    Show all records of a table
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Page number for pagination (default is 1)
      - name: per_page
        in: query
        type: integer
        required: false
        description: Number of records per page (default is 10)
      - name: format
        in: query
        type: string
        required: false
        description: Format of file
    responses:
        200:
          description: file with format
"""
    page = request.args.get('page', None, type=int)
    per_page = request.args.get('per_page', None, type=int)
    format = request.args.get('format', None, type=str)
    try:
        
        (resp, code) = get_all_records_file(table_name, page, per_page, format)
        #return {"output_file":output_file, "shp_folder" :shp_folder}, 200
        # Juste ici : dire à Flask de supprimer après réponse
        print(resp)
        
        if(code >= 300 or 200> code) :
            return jsonify({"message":json.dumps(resp)}), code 
          
        output_file = resp["output_file"]
        shp_folder = resp["shp_folder"]
    except ValueError as e:
        return {"error": str(e)}, 400
      
    
    @after_this_request
    def remove_file(response):
        try:
            os.remove(output_file)
            print(f"Fichier temporaire {output_file} supprimé.")
            if shp_folder :
              shutil.rmtree(shp_folder)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")
        return response
    # Ensuite envoyer le fichier
    return send_file(
        output_file,
        as_attachment=True,
        download_name=os.path.basename(output_file)
    )
    #return jsonify(resp),code

    
#update_data(table_name, id, data)

def update_data_by_table_name(table_name, id):
    data = request.json
    if "props" not in data :
        return jsonify({"message": "bad data format"}),400
    (resp, code) = update_data(table_name, id, data["props"])
    
    return jsonify(resp),code



def runQuery():
    """
    insert data to a table
---
parameters:
  - name: body
    in: body
    required: true
    description: body of request
    schema:
      type: object
      properties:
        props:
          type: object
          description: properties of the metadata
          example:
            table: "user"
            alias: "u"
            selectedFields: ["u.id"]
            joins: {}
            conditions: {}

responses:
  201:
    description: all data of the models
    content:
      application/json:
        examples:
          application/json:
            value:
              data: {}
    """
    data = request.json
    table = data.get("table")
    alias = data.get("alias", table[0])  # Par défaut, première lettre de la table
    selectedFields = data.get("selectedFields", ["*"])
    joins = data.get("joins", [])
    filtre = data.get("conditions", [])
    
    if not table:
        return jsonify({"error": "Table non spécifiée"}), 400

    # Construction de la requête SQL
    #l = "".replace(".", "_")
    selected_fields = ", ".join([f"{field} AS " + field.replace(".", "_") for field in selectedFields])
    query = f"SELECT {selected_fields} FROM {table} AS {alias}"
    
    join_tables = " "
        
    for i, join in enumerate(joins):
        
        tableJoin = join.get("table") 
        aliasJoin = join.get("alias") 
        onFirstJoin = join.get("onFirst") 
        onOperatorJoin = join.get("onOperator") 
        onSecondJoin = join.get("onSecond") 
        
        query += " INNER JOIN " + f"{tableJoin} AS {aliasJoin} ON {onFirstJoin} {onOperatorJoin} {onSecondJoin}"

    # Ajout des filtres
    conditions = []
    params = {}

    for i, filter in enumerate(filtre):
        field = filter.get("field")
        operator = filter.get("operator", "=")
        value = filter.get("value")

        if field and value is not None:
            param_name = f"value{i}"
            conditions.append(f"{field} {operator} :{param_name}")
            params[param_name] = value

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Exécution de la requête
    try:
        result = db.session.execute(text(query), params)
        data = [dict(row) for row in result.mappings()]
        
        return jsonify({"sql": query, "data":data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def global_search():
  """
    Recherche globale multi-entités avec filtres optionnels.

    ---
    tags:
      - Recherche
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token d'authentification Bearer. Par Exemple,  "Bearer <votre_token>"
      - name: q
        in: query
        type: string
        required: false
        description: Terme de recherche global (mot-clé).
      - name: entities
        in: query
        type: string
        required: false
        description: Liste des Noms des table à cibler (ex. centrale_electrique, projet_planifie). Si absent, recherche sur toutes.
      - name: territories
        in: query
        type: string
        required: false
        description: Liste d'IDs de territoires séparés par des virgules (ex. 1,3,5).  Si absent, recherche sur toutes.
      - name: puissance_min
        in: query
        type: number
        required: false
        description: Valeur minimale de la puissance (filtre intervalle).
      - name: puissance_max
        in: query
        type: number
        required: false
        description: Valeur maximale de la puissance (filtre intervalle).
      - name: energie_min
        in: query
        type: number
        required: false
        description: Valeur minimale de besoin energetique ou estimation consommation en energie (filtre intervalle).
      - name: energie_max
        in: query
        type: number
        required: false
        description: Valeur maximale de besoin energetique ou estimation consommation en energie (filtre intervalle).
      - name: tension_min
        in: query
        type: number
        required: false
        description: Valeur minimale de la tension electrique (filtre intervalle) (En cas de sous-stension par exemple).
      - name: tension_max
        in: query
        type: number
        required: false
        description: Valeur maximale de la tension electrique (filtre intervalle) (En cas de sous-stension par exemple).
    responses:
      200:
        description: Résultats de la recherche (dictionnaire par table).
        schema:
          type: object
          additionalProperties:
            type: array
            items:
              type: object
      400:
        description: Paramètre manquant ou invalide.
        schema:
          type: object
          properties:
            error:
              type: string
    """
  try :
    resp = get_search_model(request.args)
    return jsonify(resp), 200
  except ExceptionService as e :
    return e.get_error_message(), e.code
  