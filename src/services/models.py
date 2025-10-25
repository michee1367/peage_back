import json
from models import db
from jsonschema import validate, exceptions
from services.ExceptionService import ExceptionService
#from services.unit import get_quantities, transform_quantity_data, transform_show, getSettingsWithoutUser, transform_record
#from models.Enregistrement import Enregistrement
from sqlalchemy.inspection import inspect
from datetime import datetime, timezone
import geopandas as gpd
import pandas as pd
from shapely import wkt 
#from models.TaskImport import CSV_IMPORT_TASK, EXCEL_IMPORT_TASK, ZIP_IMPORT_TASK, JSON_IMPORT_TASK, GEOJSON_IMPORT_TASK
import shutil
import os
from flask import current_app
from sqlalchemy import func
from shapely import wkt
import math
import numbers
from sqlalchemy import or_, and_
from tools.geo import wtkToJson
from services.picture import get_pic_url
#from models.EntityAdministration.territory import Territory
from tools.objects.PaginateReturn import PaginateReturn
from tools.model import get_attr_by_path

ZIP_IMPORT_TASK = "zip"
EXCEL_IMPORT_TASK = "excel"
GEOJSON_IMPORT_TASK = "geojson"
JSON_IMPORT_TASK = "json"
CSV_IMPORT_TASK = "csv"
FILES_IMPORT_TASK = [ZIP_IMPORT_TASK, EXCEL_IMPORT_TASK, GEOJSON_IMPORT_TASK, JSON_IMPORT_TASK, CSV_IMPORT_TASK]

STOCK_TYPE_DB = "db"
STOCK_TYPE_FILE = "file"
STOCK_TYPES = [STOCK_TYPE_DB, STOCK_TYPE_FILE]
from sqlalchemy.orm import RelationshipProperty

#import json

def model_to_form_schema(model_class) :
    if not (hasattr(model_class, "__fillables__")) :
        return None
    
    fillable = getattr(model_class, "__fillables__")
    column_concerns = [*fillable, "id", "app_value"]
    
    fields = {
        column.name: str(column.type)
        for column in model_class.__table__.columns if column.name in column_concerns
    }
    
    if hasattr(model_class, "normalName"):
        normalName = model_class.normalName
    else:
        normalName = model_class.__tablename__
        
    fields_relations = get_fields_relations(model_class)
    #print(fields_relations)
        
    return {"fields":fields, "relations": get_table_relations(model_class), "normalName":normalName, "fields_relations":fields_relations}

def model_class_to_model_info(model_class) :
        if not (hasattr(model_class, "__fillables__")) :
            return None
        
        fillable = getattr(model_class, "__fillables__")
        column_concerns = [*fillable, "id", "app_value"]
        fields = {
            column.name: str(column.type)
            for column in model_class.__table__.columns if column.name in column_concerns
        }
        
        if hasattr(model_class, "normalName"):
            normalName = model_class.normalName
        else:
            normalName = model_class.__tablename__
            
        fields_relations = get_fields_relations(model_class)
            
        return {
            "fields":fields, 
            "relations": get_table_relations(model_class), 
            "normalName":normalName,
            "fields_relations":fields_relations
        }
    
    
def get_models_by_super_class(super_class) :
    models_info = {}
    if not issubclass(super_class, db.Model) :
        return models_info
    for model_class in super_class.__subclasses__():
        model_info = model_class_to_model_info(model_class)
        
        if not model_info :
            continue
        models_info[model_class.__tablename__] = model_info
        
    return models_info
        
def get_models(): 
    models_info = {}

    for model_class in db.Model.__subclasses__():
        model_info = model_class_to_model_info(model_class)
        
        if not (len(model_class.__subclasses__()) == 0) :
            sub_models_info = get_models_by_super_class(model_class) 
            models_info = {**models_info, **sub_models_info}
        
        if not model_info :
            continue
        
        models_info[model_class.__tablename__] = model_info
        
        
        
    file_path = "schema/customs/form.json"
    
    {
      "name": "donnees_socio_economiques",
      "normalName": "Données Socio-Économiques",
      "schema": {
        "title": "Données Socio-Économiques",
        "type": "object",
        "properties": {
          "activites_economiques": { "type": "string" },
          "revenu_moyen_menage": { "type": "number" },
          "capacite_payer": { "type": "number" },
          "acceptation_projet": { "type": "string" },
          "appareils_utilises_souhaites": { "type": "string" },
          "besoins_energetiques_menage": { "type": "string" },
          "ecoles_besoins_energetiques": { "type": "string" },
          "centres_sante_besoins_energetiques": { "type": "string" },
          "pme_besoins_energetiques": { "type": "string" },
          "eglises_besoins_energetiques": { "type": "string" },
          "batiments_administratifs_besoins_energetiques": { "type": "string" }
        },
        "required": [
          "activites_economiques",
          "revenu_moyen_menage"
        ]
      }
    } 
    try:
        with open(file_path) as f:
            jsonDataBrut = json.load(f)
            schemas = jsonDataBrut["schemas"]
            for schema in schemas :
                print(schema)
                properties = schema["schema"]["properties"]
                fields = {}
                
                for k, value in properties.items() :
                    print(value)
                    fields[k] = value["type"]
                
                models_info[schema["name"]] = {"fields":fields, "relations": [], "normalName": "Formulaire : " + schema["normalName"]}

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)

    return models_info

def get_table_relations(model_class):
    relations = {}

    for column in model_class.__table__.columns:
        for fk in column.foreign_keys:
            related_table = fk.column.table.name
            relations[column.name] = related_table  # Clé étrangère → Table cible

    return relations

def get_fields_relations(model_class):
    relations = {}
    if not (hasattr(model_class, "__rel_showables__")) :
        return {}
    
    rels = getattr(model_class, "__rel_showables__")
    

    # Récupérer le nom et la classe associée à chaque relationship
    relationships_info = [
        (prop.key, prop.mapper.class_)
        for prop in model_class.__mapper__.iterate_properties
        if isinstance(prop, RelationshipProperty) and prop.key in rels
    ]

    for name, related_class in relationships_info:
        #print(f"{name} → {related_class.__name__}")
        
        if not (hasattr(related_class, "__fillables__")) :
            continue
        
        fillable = getattr(related_class, "__fillables__")
        column_concerns = [*fillable, "id", "app_value"]
        
        fields = {
            column.name: str(column.type)
            for column in related_class.__table__.columns if column.name in column_concerns
        }
        relations[name] = fields
        
    return relations


def generate_jsonschema(model_class, isForModif=False):
    schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for column in model_class.__table__.columns:
        field_name = column.name
        if field_name == "id" or field_name ==  "pg_id" or field_name == "uniq_key" :
            continue
        field_type = str(column.type).lower()
        if field_name == "deleted_at" :
            print(field_type)
            #exit()
            
        #print(field_type)
        
        json_type = "string"
        if "string" in field_type:
            json_type = "string"
        elif "float" in field_type:
            json_type = "number"
        elif "integer" in field_type:
            json_type = "number"
        elif "boolean" in field_type:
            json_type = "boolean"
        elif "json" in field_type:
            json_type = "object"
        elif "array" in field_type:
            json_type = "array"
        elif "datetime" in field_type :
            json_type = "null"
        elif "date" in field_type :
            json_type = "null"
            
        schema["properties"][field_name] = {
                "anyOf": [
                    {"type": json_type},
                    {"type": "null"}
                ]
            }

        if not column.nullable and not isForModif:
            schema["required"].append(field_name)

    return schema

def tranform_tablename_to_classname(table_name) :
    return next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    

def tranform_classname_to_tablename(class_name) :
    return class_name.__tablename__
    
def get_schema(table_name):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)

    if not model_class:
        return None

    schema = generate_jsonschema(model_class)
    return schema

def get_unique_constraints(model):
    """Retourne toutes les contraintes uniques d'un modèle SQLAlchemy, y compris celles sur les colonnes."""
    mapper = inspect(model)
    table = mapper.local_table
    constraints = []

    # Récupérer les UniqueConstraint définis au niveau de la table
    for uc in table.constraints:
        if isinstance(uc, db.UniqueConstraint):
            constraints.append({
                "name": uc.name,
                "columns": [col.name for col in uc.columns]
            })

    # Vérifier les colonnes qui ont `unique=True`
    for column in table.columns:
        if column.unique:
            constraints.append({
                "name": f"unique_{column.name}",
                "columns": [column.name]
            })

    return constraints

def check_unique_constraints(model, instance, data, isForUpdate=True):
    """
    Vérifie si une autre instance que 'instance' viole une contrainte unique
    avec les nouvelles valeurs définies dans 'data'.
    """
    constraints = get_unique_constraints(model)
    
    for constraint in constraints:
        filter_args = []
        
        for column in constraint["columns"]:
            if column in data:  # Vérifier si la colonne est modifiée
                filter_args.append(getattr(model, column) == data[column])
        
        if not filter_args:
            continue  # Si aucune colonne pertinente dans `data`, on ignore

        query = db.session.query(model).filter(*filter_args)
        
        # Exclure l'instance en cours de modification
        if instance.id and isForUpdate:
            query = query.filter(model.id != instance.id)

        # Vérifier s'il existe déjà une autre entrée avec ces valeurs uniques
        if db.session.query(query.exists()).scalar():
            raise ExceptionService("Violation contraint unique : " + json.dumps(constraint), 400)  # Conflit détecté

    return None  # Pas de conflit, on peut modifier

def update_instance(model, instance, data):
    """
    Met à jour une instance SQLAlchemy en respectant les contraintes uniques.
    """
    check_unique_constraints(model, instance, data)

    for key, value in data.items():
        if hasattr(instance, key):  # Vérifier si l'attribut existe
            setattr(instance, key, value)

    return instance

def clean_nan_values(d):
    if isinstance(d, dict):
        return {k: clean_nan_values(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_nan_values(v) for v in d]
    elif isinstance(d, numbers.Number):
        if isinstance(d, float) and (math.isnan(d) or math.isinf(d)):
            return None
        return d
    else:
        return d
    
def clean_values(data, schema, fillables) :
    data_cleaned = clean_nan_values(data)
    data_proccessing = {}
    
    for key,value in schema["properties"].items() :
        try :
            field_type = value["anyOf"][0]["type"]
            
            if not (key in fillables) :
                continue
            
            
            if "string" in field_type:
                #print(field_type)
                #exit()
                data_cleaned[key] = str(data_cleaned[key])
            elif "number" in field_type:
                data_cleaned[key] = float(data_cleaned[key])
            elif "integer" in field_type:
                data_cleaned[key] = int(data_cleaned[key])
            elif "boolean" in field_type:
                data_cleaned[key] = bool(data_cleaned[key])
            elif "object" in field_type:
                data_cleaned[key] = json.loads(data_cleaned[key])
                #json_type = "json"
            elif "array" in field_type:
                #print(data_cleaned[key])
                data_cleaned[key] = str(data_cleaned[key]).split(",") # json.loads(data_cleaned[key])
                #data_cleaned[key] = bool(data_cleaned[key])
                #json_type = "array"
            elif "null" in field_type:
                data_cleaned[key] = None
                
            data_proccessing[key] = data_cleaned[key]
                
        except Exception as err :
            print(err)
            #exit()
            pass
        
    data_cleaned = data_proccessing
    return data_cleaned


def clean_and_transform_data(table_name, data) :
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)

    if not model_class:
        raise ExceptionService("Model not found", 404)  # Conflit détecté

    if not (hasattr(model_class, "__fillables__")) :
        raise ExceptionService("Model not fillable", 400)  # Conflit détecté
    
    fillables = model_class.__fillables__
    
    schema = generate_jsonschema(model_class)
    data_cleaned = clean_values(data,schema, fillables)
    
    """if unit_settings :
        settings = unit_settings
    else :
        settings = getSettingsWithoutUser()
        
    data_record = transform_record(model_class,settings,data_cleaned)
    data_show = transform_show(model_class,settings,data_record)"""
    
    data_show = data_cleaned
    
    if data.get("id") :
        data_show["id"] = data["id"]
        
    if data.get("geometry") :
        data_show["geometry"] = data["geometry"]
        
    if data.get("geom") :
        data_show["geom"] = data["geom"]
        
    
    return data_show


def insert_data(table_name, data, unit_settings=None):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)

    if not model_class:
        return {"error": "Model not found"}, 404

    if not (hasattr(model_class, "__fillables__")) :
        return {"error": "Model not fillable"}, 400
    
    fillables = model_class.__fillables__
    
    schema = generate_jsonschema(model_class)

    try:
        data_cleaned = clean_nan_values(data)
        data_proccessing = {}
        #print(schema)
        #{k: clean_nan_values(v) for k, v in d.items()}
        #print("data_cleaned")
        #print(data_cleaned)
        #print("data_cleaned")
        
        for key,value in schema["properties"].items() :
            try :
                field_type = value["anyOf"][0]["type"]
                
                if not (key in fillables) :
                    continue
                
                if "string" in field_type:
                    #print(field_type)
                    #exit()
                    data_cleaned[key] = str(data_cleaned[key])
                elif "number" in field_type:
                    data_cleaned[key] = float(data_cleaned[key])
                elif "integer" in field_type:
                    data_cleaned[key] = int(data_cleaned[key])
                elif "boolean" in field_type:
                    data_cleaned[key] = bool(data_cleaned[key])
                elif "object" in field_type:
                    data_cleaned[key] = json.loads(data_cleaned[key])
                    #json_type = "json"
                elif "array" in field_type:
                    #print(data_cleaned[key])
                    data_cleaned[key] = str(data_cleaned[key]).split(",") # json.loads(data_cleaned[key])
                    #data_cleaned[key] = bool(data_cleaned[key])
                    #json_type = "array"
                elif "null" in field_type: 
                    data_cleaned[key] = None
                    
                data_proccessing[key] = data_cleaned[key]
                    
            except Exception as err :
                print(err)
                #exit()
                pass
            
        data_cleaned = data_proccessing
        
        validate(instance=data_cleaned, schema=schema)
        #print(data_cleaned)
        #exit()
        
        """if unit_settings :
            settings = unit_settings
        else :
            settings = getSettingsWithoutUser()
        
        data_cleaned = transform_record(model_class,settings,data_cleaned)"""
        #print("#######################")
        #print(data_cleaned)
        #print("#######################")
        #return {"message": "Data inserted successfully"}, 201
        print(data.get("geom"))
        exit()
        new_record = Enregistrement(
            #uniq_key="clé_unique_123",
            #geom='POINT(2.2945 48.8584)',  # Si tu utilises GeoAlchemy2, utilise WKT ou WKB
            geom=data.get("geom"),  # Si tu utilises GeoAlchemy2, utilise WKT ou WKB
            props=data_cleaned,
            other_data={},
            nom_table=table_name,
            #user_id=1,
            created_at=datetime.now(timezone.utc),
            deleted_at=None,
            #validated_at=datetime.now(timezone.utc)  # ou None si pas encore validé
        )

        #new_record = model_class(**data)
        db.session.add(new_record)
        db.session.commit()
        print("Success")

        return {"message": "Data inserted successfully"}, 201
    except exceptions.ValidationError as e:
        print("###########Failled################")
        print(e)
        db.session.rollback()
        #return {"error": "Validation failed", "details": e.message}, 400
        # Obtenir le chemin complet vers l'erreur
        print(data_cleaned)
        path = ".".join([str(p) for p in e.path])  # ex: "adresse.ville"
        return {
            "error": "Validation failed",
            "property": path,
            "message": e.message
        }, 400
    except Exception as e:
        print("###########Failled################")
        print(e)
        print(data_cleaned)
        #print(data_cleaned)
        #exit()
        #db.session.rollback()
        db.session.rollback()
        return {"error": "Insertion failed", "details": str(e)}, 500
""" 
def validate_data_db(table_name, id, data) :
    
    record = Enregistrement.query.filter_by(id=id, nom_table=table_name).first()
    
    if not record:
        return {"error": "Enregistrement n'exist pas"}, 404
    data = {}
    props = getattr(record, "props", {})
    
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)

    if not model_class:
        file_path = "schema/customs/form.json"
        with open(file_path) as f:
            jsonDataBrut = json.load(f)
            schemas = jsonDataBrut["schemas"]
            schema_entry = next((item for item in schemas if item["name"] == table_name), None)
            if not schema_entry:
                return {"message": "Form or Model not found"}, 404
            
            record.validated_at = datetime.now(timezone.utc)
            
            db.session.commit()
            
            return {"message": "Data validated successfully"}, 201
    
    if not (hasattr(model_class, "__fillables__")) :
        return {"error": "Model not fillable"}, 400
    
    schema = generate_jsonschema(model_class)
    fillables = model_class.__fillables__
    
    for key,value in props.items() :
        if not (key in fillables) :
            continue
        data[key] = value
        
    try:
        validate(instance=data, schema=schema)
        
        for key in data :
            if data[key] == "None" :
                data[key] = None
                
        att_territory = getattr(model_class,"__att_terrirory__", None)
        
        if att_territory :
            att = att_territory.get("att", None)
            if att :
                point = data.get("geom", None)
                territory = get_territory(point)
                if territory :
                    data[att] = getattr(territory, "id")
        
        models_impact = getattr(model_class,"__models_impact__", [])
        
        for model_impact in models_impact :
            model = get_model_name(model_impact.get("table_name"))
            
            query = db.session.query(model)
            #print(model)
            field = getattr(model, model_impact.get("impact_model_att_name"), None)
            query = query.filter(field == data.get(model_impact.get("att_name")))
            entity = query.first()
            
            if not entity :
                continue
                {"message":"projet planifier n'existe pas"}, 400
            
            method = getattr(entity, model_impact.get("method_name"))
            
                        
        new_record = model_class(**data)
        
        if getattr(new_record, "geom", None) :
            new_record.geom = record.geom
        
        if hasattr(new_record, "setUniqKey") :
            new_record.setUniqKey()
            
        db.session.add(new_record)
        
        record.deleted_at = datetime.now(timezone.utc)
        record.validated_at = datetime.now(timezone.utc)
        
        
        db.session.commit()
        
        for model_impact in models_impact :
            model = get_model_name(model_impact.get("table_name"))
            
            query = db.session.query(model)
            field = getattr(model, model_impact.get("impact_model_att_name"), None)
            query = query.filter(field == data.get(model_impact.get("att_name")))
            entity = query.first()
            
            if not entity :
                continue
            
            method = getattr(entity, model_impact.get("method_name"))
            method(new_record)

        db.session.commit()
        return {"message": "Data inserted successfully"}, 201
    except exceptions.ValidationError as e:
        return {"error": "Validation failed", "details": e.message}, 400
    except Exception as e:
        return {"error": "Insertion failed", "details": str(e)}, 500
"""

def validate_data_file(table_name, id, data) :
        return {"error": "Not supported yet"}, 400
    
    
def save_data(table_name, data) :
    data = clean_and_transform_data(table_name, data)
    
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    schema = generate_jsonschema(model_class)
    try :
            
        validate(instance=data, schema=schema)
        
        for key in data :
            if data[key] == "None" :
                data[key] = None
        
        models_impact = getattr(model_class,"__models_impact__", [])
        
        for model_impact in models_impact :
            model = get_model_name(model_impact.get("table_name"))
            
            query = db.session.query(model)
            #print(model)
            field = getattr(model, model_impact.get("impact_model_att_name"), None)
            query = query.filter(field == data.get(model_impact.get("att_name")))
            entity = query.first()
            
            if not entity :
                continue
                {"message":"projet planifier n'existe pas"}, 400
            
            method = getattr(entity, model_impact.get("method_name"))
            
                        
        new_record = model_class(**data)
        
        if getattr(new_record, "geom", None) :
            new_record.geom =  data.get("geom")
            
        
        if hasattr(new_record, "setUniqKey") :
            new_record.setUniqKey()
            
        db.session.add(new_record)        
        
        db.session.commit()
        
        for model_impact in models_impact :
            model = get_model_name(model_impact.get("table_name"))
            
            query = db.session.query(model)
            field = getattr(model, model_impact.get("impact_model_att_name"), None)
            query = query.filter(field == data.get(model_impact.get("att_name")))
            entity = query.first()
            
            if not entity :
                continue
            
            method = getattr(entity, model_impact.get("method_name"))
            method(new_record)

        db.session.commit()
        return {"message": "Data inserted successfully", "entityId":new_record.id}, 201
    except exceptions.ValidationError as e:
        return {"error": "Validation failed", "details": e.message}, 400
    except Exception as e:
        return {"error": "Insertion failed", "details": str(e)}, 500
    

    
    
"""
def validate_data(table_name, id, data):
    
    listId = str(id).split("-")
    try :
        normalId = int(listId[-1])
    except :
        return {"error": "Bad ID"}, 400
    
    if len(listId) == 1 :
        return validate_data_db(table_name, normalId, data)
    elif len(listId) >= 2 :
        stock_type = str(listId[0])
        if not (stock_type in STOCK_TYPES) :
            return {"error": "Bad ID"}, 400
        
        if stock_type == STOCK_TYPE_DB :
            return validate_data_db(table_name, normalId, data)
        
        if stock_type == STOCK_TYPE_FILE :
            return validate_data_file(table_name, id, data)
            
    elif len(listId) > 3 :
        return {"error": "Bad ID"}, 400
    
    
def delete_data(table_name, id):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)

    if not model_class:
        return {"error": "Model not found"}, 404
    
    record = Enregistrement.query.filter_by(id=id, nom_table=table_name).first()
    
    if not record:
        return {"error": "Enregistrement n'exist pas"}, 404
    

    try:
        
        record.deleted_at = datetime.now(timezone.utc)
        #record.validated_at = datetime.now(timezone.utc)
        
        db.session.commit()

        return {"message": "Data inserted successfully"}, 201
    except exceptions.ValidationError as e:
        return {"error": "Validation failed", "details": e.message}, 400
    except Exception as e:
        return {"error": "Insertion failed", "details": str(e)}, 500
""" 
    
def update_data(table_name, id, data):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)

    if not model_class:
        return {"error": "Model not found"}, 404
    
    record = model_class.query.filter_by(id=id).first()
    
    if not record :
        return {"error": "not found"}, 404
    
    schema = generate_jsonschema(model_class, True)

    try:
        form_schema = model_to_form_schema(model_class)
        
        if not form_schema :
            return {"error": "Model : unsupported yet"}, 400
        
        if  form_schema.get("relations") :
            relations = form_schema.get("relations")
            for key in relations :
                table_relation = relations[key]
                schema_relation = tranform_tablename_to_classname(table_relation)
                #print(schema_relation)
                if not schema_relation :
                    return {"error": "Model : unsupported yet"}, 400
                if data[key] :
                    entity_relation = schema_relation.query.filter(schema_relation.id == data[key]).first()
                    #print(entity_relation)
                    if not entity_relation :
                        return {"error": "Model : record "+ str(table_relation) + " with id :" + str (data[key]) + " no exiss"}, 422
                        
     
        fillables = model_class.__fillables__
        data = clean_values(data, schema, fillables)
        #return schema, 400
        validate(instance=data, schema=schema)
        
        """settings = getSettingsWithoutUser()
            
        data = transform_record(model_class,settings,data)"""
        
        update_instance(model_class, record, data)

        db.session.commit()

        return {"message": "Data update successfully"}, 201
    except exceptions.ValidationError as e:
        return {"error": "Validation failed", "details": e.message}, 400
    except Exception as e:
        return {"error": "update failed", "details": str(e)}, 500
"""
def get_all_records_enr(table_name, page=1, per_page=10) -> PaginateReturn:
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    
    #records = model_class.query.all()
    #records = Enregistrement.query.filter_by(nom_table=table_name).all()
    
    pagination = Enregistrement.query.filter(
        Enregistrement.deleted_at.is_(None),
        Enregistrement.validated_at.is_(None),
        Enregistrement.nom_table == table_name
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    #pagination = Enregistrement.query.paginate(page=page, per_page=per_page, error_out=False)
    
    #return {"data":[record_brute_to_dict(record) for record in records]}, 200
    #return {"data":[record_to_dict(record) for record in records]}, 200
    #if not model_class:
    #        return {"error": "Model not found"}, 404

    # Récupérer page et per_page depuis les paramètres GET
    #page = request.args.get('page', 1, type=int)
    #per_page = request.args.get('per_page', 10, type=int)

    #pagination = model_class.query.paginate(page=page, per_page=per_page, error_out=False)
    records = pagination.items
    dataBrut = [record_to_dict(record) for record in records]
    data = []
    settings = getSettingsWithoutUser()
    #transform_show
    
    for itemBrut in dataBrut :
        
        item = itemBrut["props"]
        if model_class :
            item = transform_show(model_class, settings, item)
        
        if item.get("image") :
            item["image"] = None
            
        item["id"] = itemBrut["id"]
        data.append(item)
    
    return PaginateReturn(data, pagination.page, pagination.per_page, pagination.total)
        
    return {
        "data": data,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }
"""

"""
def get_all_records(table_name, page=1, per_page=10) -> PaginateReturn:
    
    result = get_all_records_enr(table_name, page, per_page)
    
    return result
"""

def get_all_records_file(table_name, page=None, per_page=None, file_format="geojson"):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    
    if not model_class:
        return {"error": "Model not found"}, 404

    #pagination = model_class.query.paginate(page=page, per_page=per_page, error_out=False)
    #records = pagination.items
    if not page and not per_page :
        records = model_class.query.all()
        page = 1
    else :
        if not page :
            page = 1
        if not per_page :
            per_page = 10
        pagination = model_class.query.paginate(page=page, per_page=per_page, error_out=False)
        records = pagination.items
        

    records_list = [record_to_dict_with_geom(record) for record in records]

    if not records_list:
        return {"error": "No data found"}, 404

    df = pd.DataFrame(records_list)

    # Utiliser le nouvel exporteur
    
    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    filename_base = f"{table_name}_page_{page}"
    
    filename_base = os.path.join(UPLOAD_FOLDER, filename_base)
    
    try:
        output_file, shp_folder = export_to_format(df, file_format, filename_base)
    except ValueError as e:
        return {"error": str(e)}, 400

    return {"output_file":output_file, "shp_folder" :shp_folder}, 200



def export_to_format(df, file_format, filename_base):
    """Exporte un DataFrame ou GeoDataFrame vers le format demandé """

    # Si geometry est dans les colonnes, construire un GeoDataFrame
    if 'geometry' in df.columns:
        df['geometry'] = df['geometry'].apply(lambda x: wkt.loads(x) if isinstance(x, str) else x)
        gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    else:
        gdf = gpd.GeoDataFrame(df)

    output_file = ""
    shp_folder = None

    if file_format == GEOJSON_IMPORT_TASK:
        output_file = f"{filename_base}.geojson"
        gdf.to_file(output_file, driver='GeoJSON')

    elif file_format == CSV_IMPORT_TASK:
        output_file = f"{filename_base}.csv"
        gdf.drop(columns='geometry', errors='ignore').to_csv(output_file, index=False)

    elif file_format == EXCEL_IMPORT_TASK:
        output_file = f"{filename_base}.xlsx"
        gdf.drop(columns='geometry', errors='ignore').to_excel(output_file, index=False)

    elif file_format == JSON_IMPORT_TASK:
        output_file = f"{filename_base}.json"
        gdf.drop(columns='geometry', errors='ignore').to_json(output_file, orient='records')

    elif file_format == ZIP_IMPORT_TASK:
        # Exporter en Shapefile
        shp_folder = f"{filename_base}_shapefile"
        gdf.to_file(shp_folder, driver='ESRI Shapefile')
        shutil.make_archive(shp_folder, 'zip', shp_folder)
        output_file = f"{shp_folder}.zip"

    else:
        raise ValueError(f"Unsupported format: {file_format}")

    return output_file, shp_folder



def get_records_save(table_name, record_id):
    """ Récupère un enregistrements d'un modèle SQLAlchemy """
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    #print(model_class)
    if not model_class:
        raise ExceptionService("Model n'existe pas", 404)
         
    else :
        
        filters_null = getattr(model_class,"__filters_null__", [])
                    
        query = model_class.query
                
        for filter_null in filters_null :
            attName = filter_null.get("att", None)
            if not attName :
                continue
            field = getattr(model_class, attName, None)
            if not field :
                continue
            query = query.filter(and_(field.is_(None)))
            
        entity = query.filter(model_class.id == record_id).first()
        
        #print(entity)
    
        if entity :
            data = record_to_dict(entity)
                
            
            
        else :
            data = None
            
            
    if not data :
        return {
            "message":"Record not found"
        }, 404


    if model_class :
        #settings = getSettingsWithoutUser()
        #data = transform_show(model_class, settings, data)
        if data.get("id") :
            data["pic_url"] = get_pic_url(table_name,str(data.get("id")))
        
        #data = transform_show(model_class, settings, data)
    
    return {
        "data":data
    }, 200
        

def get_all_records_save(table_name, page=1, per_page=10, isShort=False):
    """ Récupère tous les enregistrements d'un modèle SQLAlchemy """
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    
    if not model_class:
        
        raise ExceptionService("Model n'existe pas", 404)
    
    else :
        
        filters_null = getattr(model_class,"__filters_null__", [])
                    
        query = model_class.query
        
        
        for filter_null in filters_null :
            attName = filter_null.get("att", None)
            if not attName :
                continue
            field = getattr(model_class, attName, None)
            if not field :
                continue
            query = query.filter(and_(field.is_(None)))
            
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        records = pagination.items
    
        if isShort :
            data = []
            for record in records :
                wording = None
                if hasattr(record, 'getWording'):
                    wording = record.getWording()
                    print("La méthode existe.")
                else:
                    wording = str(record)
                    print("La méthode n'existe pas.")
                
                data.append({
                    "id":record.id,
                    "wording":wording
                })
        else :
            data = [record_to_dict(record) for record in records]


    if model_class :
        #settings = getSettingsWithoutUser()
        #data = [transform_show(model_class, settings, item) for item in data]
        
        for item in data :
            #print(item)
            if item.get("id") :
                item["pic_url"] = get_pic_url(table_name,str(item.get("id")))
        #item = transform_show(model_class, settings, item)
    
    return {
        "data":data,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }, 200
    

def record_to_dict(record, widthRel=False):
    """ Convertit un objet SQLAlchemy en dictionnaire """
    print(record.__table__.columns)
    
    if not (hasattr(record, "__showables__")) :
        showables = []
    else :
        showables = record.__showables__
        
    
    if not (hasattr(record, "rel_showables")) :
        rel_showables = []
    else: 
        rel_showables = record.__rel_showables__
    
    data = {}
    
    for column in record.__table__.columns :
        if column.name in showables :
            data[column.name] = getattr(record, column.name, None)
            continue
            
    for rel in rel_showables :
        value = getattr(record, rel, None)
        if not value :
            data[rel] = value
            continue
        elif isinstance(value, db.Model) :
            data[rel] = record_to_dict(value, widthRel)
            continue
        
        data[rel] = value
    data["id"] = record.id 
    
    if(getattr(record,"getWording", None)) :
        data["app_value"] = getattr(record,"getWording", None)()
    else :
        data["app_value"] = record.id
        
    return data


def record_to_dict_with_geom(record):
    """ Convertit un objet SQLAlchemy en dictionnaire """
    #print(record.puissance_installee)
    #exit()
    data = {column.name: getattr(record, column.name) for column in record.__table__.columns}
    if "geom" in data :
        wkt_data = db.session.query(func.ST_AsText(record.geom)).scalar()
        # Convertir WKT en géométrie Shapely
        geometry = wkt.loads(wkt_data)
        data["geometry"] =  geometry
        data["geom"] = None
        
    return data

def grecord_to_dict_geojson(record) :
    data = {column.name: getattr(record, column.name) for column in record.__table__.columns if column.name != "geom"}
    if(getattr(record,"getWording", None)) :
        data["app_value"] = getattr(record,"getWording", None)()
    geometry = {
                "type": "Point",
                "coordinates":(0,0)
            }
    if getattr(record, "geom", None) :
        
        wkt = db.session.query(func.ST_AsText(record.geom)).scalar()
                    
        if wkt :
            geometry = wtkToJson(wkt)
        
    dataFeature = {
        "type": "Feature",
        "geometry": geometry,
        "properties": data
    }
    return dataFeature
def record_brute_to_dict(record):
    """ Convertit un objet SQLAlchemy en dictionnaire """
    data = record.props
    data["id"] = record.id
    data["created_at"] = record.created_at
    data["deleted_at"] = record.deleted_at
    data["validated_at"] = record.validated_at
    
    return data

def get_search_model(args) :
    
    query = args.get("q", "").strip().lower()
    entity_names = args.get("entities")  # Nouveau paramètre
    entity_names = [str(ename) for ename in entity_names.split(",")] if entity_names else None  # Nouveau paramètre

    territory_ids = args.get("territories")
    territory_ids = [int(rid) for rid in territory_ids.split(",")] if territory_ids else None

    numeric_filters = {}
    

    if not query:
        query = None
        #raise ExceptionService("Missing query parameter 'q'", 400)
    
    model_classes = db.Model.__subclasses__()
    #model_table_names = [{}]
    if entity_names and len(entity_names) :
        model_classes = [model_class for model_class in model_classes if model_class.__tablename__ in entity_names]
        
    #print(model_classes)
    resp = {}
    for model_class in model_classes :
        table_name = model_class.__tablename__
        data_result_brut = search_model(model_class, query, territory_ids, numeric_filters)
        for item in data_result_brut :
            #print(item)
            if item.get("properties") :
                properties = item.get("properties")
                if properties.get("id") :
                    item["properties"]["pic_url"] = get_pic_url(table_name,str(properties.get("id")))
        resp[table_name] = data_result_brut
        
    #for model_class in db.Model.__subclasses__():
    #print(resp)
    return {"query":query,"territory_ids":territory_ids, "numeric_filters":numeric_filters, "entity_names":entity_names, "data":resp}
    

def search_model(model, query_string=None, region_ids=None, numeric_filters=None, limit=10):
    print(model)
    if not hasattr(model, '__search__'):
        return []
    
    if not query_string and not region_ids and not numeric_filters :
        return []

    filters = []
    # Filtre texte
    query = db.session.query(model)
    
    if query_string :
        for field_name in model.__search__:
            field = getattr(model, field_name, None)
            if field is not None:
                filters.append(field.ilike(f"%{query_string}%"))

        query = query.filter(or_(*filters))
        
    filters_null = getattr(model,"__filters_null__", [])
                
    #query = model.query
    
    
    for filter_null in filters_null :
        attName = filter_null.get("att", None)
        
        if not attName :
            continue
        field = getattr(model, attName, None)
        
        if not field :
            continue
        query = query.filter(and_(field.is_(None)))
        #print(query)

    return [grecord_to_dict_geojson(obj) for obj in query.limit(limit).all()]
    # Filtre régions
    if region_ids and hasattr(model, '__region_field__'):
        region_path = model.__region_field__
        try:
            region_attr = eval("model." + ".".join(region_path.split(".")))
            
            query = query.join(region_path.split(".")[0]).filter(region_attr.in_(region_ids))
        except Exception as e:
            print(f"[ERROR] Erreur d'accès à region_id: {e}")

    # Filtre numérique sur intervalles
    if numeric_filters and hasattr(model, '__numeric_filters__'):
        for field_name in model.__numeric_filters__:
            if field_name in numeric_filters:
                field = getattr(model, field_name, None)
                if field is not None:
                    min_val, max_val = numeric_filters[field_name]
                    if min_val is not None:
                        query = query.filter(field >= min_val)
                    if max_val is not None:
                        query = query.filter(field <= max_val)

    return [record_to_dict_with_geom(obj) for obj in query.limit(limit).all()]


def get_structure(table_name):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    if not model_class :
        return {}
    fields = {
            column.name: str(column.type)
            for column in model_class.__table__.columns #if column.name != "id"
        }
    return fields

def is_geom(table_name) :
    fields = get_structure(table_name)
    if not fields : 
        return False
    
    return "geom" in fields and fields["geom"].find("geometry") !=-1

def get_model_name(table_name):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    return model_class
    
    
def get_model_name_by_class(class_name):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == class_name), None)
    return model_class

"""
def get_territory(point) :
    territories = Territory.query.filter(func.ST_Contains(Territory.geom, point)).all()
    terrSearch = None
    if len(territories) == 0 :
        #print("Pas de province")
        terrSearch = None
        #print(point)
        #exit()
        #return (2, data["nom_du_projet"])
    else :
        #exit()
        #print(data)
        terrSearch = territories.pop()
        
    return terrSearch
""" 
    

def get_model_columns(model):
    return [c for c in inspect(model).mapper.column_attrs]