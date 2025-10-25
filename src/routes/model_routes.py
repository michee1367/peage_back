from flask import Blueprint
from controllers.ModelController import getAllModels, get_schema_by_table_name, insert_data_by_table_name, \
  update_data_by_table_name, runQuery, \
    get_all_records_by_table_name_download, get_all_save_records_by_table_name, global_search, get_save_records_by_table_name
    
from hashlib import pbkdf2_hmac

model_api = Blueprint('model_api', __name__)

model_api.route('/all', methods=['GET'])(getAllModels)

@model_api.route('/schema/<table_name>', methods=['GET'])
def get_model_by_tablename(table_name):
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
    return get_schema_by_table_name(table_name)


@model_api.route('/insert/<table_name>', methods=['POST'])
def insert_data_by_tablename(table_name):
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
    return insert_data_by_table_name(table_name)


  

@model_api.route('/records/<table_name>/save', methods=['GET'])
def get_all_save_records_by_tablename(table_name):
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
      - name: table_name
        in: path
        type: string
        required: true
        description: Le nom de la table pour laquelle les enregistrements doivent être récupérés
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
  return get_all_save_records_by_table_name(table_name)
  

@model_api.route('/records/<table_name>/download', methods=['GET'])
def get_all_records_by_tablename_download(table_name):
    """
    Récupère tous les enregistrements d'une table et renvoie un fichier dans le format demandé (geojson, shapefile, etc.)

    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Numéro de la page pour la pagination (par défaut 1)
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        description: Nombre d'enregistrements par page (par défaut 10)
        default: 10
      - name: format
        in: query
        type: string
        required: false
        description: "Format du fichier à générer. Les options possibles sont : 'geojson', 'csv', 'json', 'shapefile', etc."
        enum: [geojson, csv, json, zip, excel]
        default: geojson
      - name: table_name
        in: path
        type: string
        required: true
        description: Le nom de la table pour laquelle les enregistrements doivent être récupérés

    responses:
        200:
          description: Fichier contenant les enregistrements de la table dans le format demandé
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary
        404:
          description: Table non trouvée ou aucune donnée disponible
        400:
          description: Format de fichier invalide ou autre erreur liée aux paramètres
    """
    return get_all_records_by_table_name_download(table_name)

@model_api.route('/update/<table_name>/<id>', methods=['POST'])
def update_data_by_tablename(table_name, id):
    """
    update data to a table
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
  - name: id
    in: path
    type: integer
    required: true
    description: id for record

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
    return update_data_by_table_name(table_name, id)
  

model_api.route('/query/run/data', methods=['POST'])(runQuery)


#import_data

  
#def validate_data_table_name(table_name, id, data):

model_api.route('/search', methods=['GET'])(global_search)
