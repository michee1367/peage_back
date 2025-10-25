import json
from models import db
from models.User import User
from jsonschema import validate, exceptions
from services.ExceptionService import ExceptionService
from tools.role import get_all_roles
#from services.notification_service import create_notification, create_notification_by_user
from flask import g
entitySchemaUpdate = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "nom": {"type": "string"},
        "post_nom":{
            "type": "string",
        },
        "prenom": {
            "type": "string"
        },
        "picture": {"type": "string"},
        "roles": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": []
            }
        }
    },
    "required": []
}

#HIERARCHY_ROLES

def create_logic(user_info):
    try:
        user = User.query.filter_by(email=user_info["email"]).first()
        #create_notification("Création d'un compte : "+ user_info["nom"]+" "+user_info["post_nom"]+" "+user_info["post_nom"], "ROLE_LEVEL_1")
        
        if user is None :
            user = User(
                            uniq_key=user_info["email"],
                            email=user_info["email"],
                            nom=user_info["nom"] if "nom" in user_info else None,
                            post_nom=user_info["post_nom"] if "post_nom" in user_info else None,
                            prenom=user_info["prenom"] if "prenom" in user_info else None,
                            picture=user_info["picture"] if "picture" in user_info else None,
                            other_data=user_info["other_data"] if "other_data" in user_info else {},
                            roles=user_info["roles"] if "roles" in user_info else ["ROLE_USER"],
                        )

            #print(record)
            #exit(1)
            print("####Save####")
            db.session.add(user)
            db.session.commit()
            """try:
                create_notification("Création d'un compte : "+ user_info["nom"]+" "+user_info["post_nom"]+" "+user_info["post_nom"], "ROLE_LEVEL_1")
            except e :
                pass"""
        return user

    except Exception as e:
        print(e)
        return None
  
def all_user():
    
    try:        
        records = User.query.all()
        data = []
        for record in records :
            #print(wkt)
            #exit()
            item = {}
            item["email"] = record.email
            item["nom"] = record.nom
            item["post_nom"] = record.post_nom
            item["prenom"] = record.prenom
            item["picture"] = record.picture
            item["other_data"] = record.other_data
            item["roles"] = record.getRoles()
            #province
            item["id"] = record.id
            
            data.append(item)
            
        return data

    except exceptions.ValidationError as err:
        #print("JSON invalide:", err.message)
        raise ExceptionService(err.message, 422)   

def update_logic(id, user_info):
    try:
        roles = get_all_roles()
        #print(roles)
        entitySchemaUpdate["properties"]["roles"]["items"]["enum"] = roles
        validate(instance=user_info, schema=entitySchemaUpdate)

        email = user_info["email"] if "email" in user_info else None
        userEmail = User.query.filter_by(email=email).first()
        user = User.query.filter_by(id=id).first()
        
        if user is None :
            return None
        
        if (userEmail is not None) and (userEmail.id != user.id) : 
            return None
        
        user.uniq_key=user_info["email"]
        user.email=user_info["email"]
        user.nom=user_info["nom"] if "nom" in user_info else user.nom,
        user.post_nom=user_info["post_nom"] if "post_nom" in user_info else user.post_nom,
        user.prenom=user_info["prenom"] if "prenom" in user_info else user.prenom
        user.picture=user_info["picture"] if "picture" in user_info else user.picture
        user.other_data=user_info["other_data"] if "other_data" in user_info else user.other_data
        user.roles=user_info["roles"] if "roles" in user_info else user.roles
        
        db.session.commit()
        
        print("###update###")
        """try:
        
            #create_notification("Modification d'un compte : (ID: "+ str(user.id) +")"+user_info["nom"]+" "+user_info["post_nom"]+" "+user_info["post_nom"], "ROLE_LEVEL_1")
            #create_notification_by_user("Modification de votre compte", user.id)
            
        except e :
        #    print(e)
            pass"""
            
        return {"message": "Data update successfully"}, 201
        

    except exceptions.ValidationError as e:
        print(e.message)
        return {"error": "Validation failed", "details": e.message}, 400
    except Exception as e:
        print(e)
        return {"error": "Insertion failed", "details": str(e)}, 500
      
def get_user_by_id(user_id) :
    return User.query.filter(User.id == user_id).first()

def get_user() :
    #print("user")
    try :
        return g.current_user
    except Exception as e :
        return None
    #return User.query.first()

def show_logic(id):
    try:
        record = User.query.filter_by(id=id).first()
        item = {}
        item["email"] = record.email
        item["nom"] = record.nom
        item["post_nom"] = record.post_nom
        item["prenom"] = record.prenom
        item["picture"] = record.picture
        item["other_data"] = record.other_data
        item["roles"] = record.getRoles()
        #province
        item["id"] = record.id
        return item, 200
        
    except exceptions.ValidationError as e:
        return {"error": "Validation failed", "details": e.message}, 400
    except Exception as e:
        return {"error": "Insertion failed", "details": str(e)}, 500