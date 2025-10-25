import json
from flask import current_app
import os
from jsonschema import validate, exceptions
from models import db
from services.ExceptionService import ExceptionService
from services.user_service import get_user
from models.Pic import Pic
from datetime import datetime, timezone
from tools.str_tools import generer_chaine_alea
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import base64

FOLDER_CONFIG_PARAM = "FOLDER_PIC"
HOSNAME_CONFIG_PARAM = "PICTURE_HOSTNAME"
    
def get_pic_path(table_name, recordID) :
    try:
        
        pic = Pic.query.filter(Pic.enregistrement_id == recordID and Pic.nom_table == table_name).first()
        if pic :
            return table_name +"/"+ pic.nom  
        
        return get_default_rel_path()
                    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ExceptionService("Schema file problem", 500)
        
    except Exception as e:
        raise ExceptionService(e.args[0], 500)

def get_pic_url(table_name, recordID) :
    return path_rel_to_url(get_pic_path(table_name, recordID))
    
def get_dirname(table_name) :
    
        FOLDER = current_app.config[FOLDER_CONFIG_PARAM]
        os.makedirs(FOLDER, exist_ok=True)
        
        table_dirname = os.path.join(FOLDER, table_name)
        
        return table_dirname

def get_default_dirname() :
    
        FOLDER = "pictures/"
        os.makedirs(FOLDER, exist_ok=True)
        
        #table_dirname = os.path.join(FOLDER, "default.png")
        
        return FOLDER
    
def path_rel_to_url(path_rel):
    if path_rel :
        HOSTNAME = current_app.config[HOSNAME_CONFIG_PARAM]
        return  HOSTNAME +"/pics/"+path_rel
    
def get_default_url():
    HOSTNAME = current_app.config[HOSNAME_CONFIG_PARAM]
    return  HOSTNAME + "/pics/"+get_default_rel_path()
def get_default_rel_path():
    #HOSTNAME = current_app.config[HOSNAME_CONFIG_PARAM]
    return  "others/storages/default"
    
    
def change_picture_record(table_name, recordID, file) :
    try:
        FOLDER = current_app.config[FOLDER_CONFIG_PARAM]
        os.makedirs(FOLDER, exist_ok=True)
        
        table_dirname = os.path.join(FOLDER, table_name)
        
        os.makedirs(table_dirname, exist_ok=True)
        
        filename_arr = secure_filename(file.filename).split(".")
        filename = ("-".join(filename_arr[0:-1]) + "-" + generer_chaine_alea(5) +".").lower() + filename_arr[-1]
        
        
        file_path = os.path.join(table_dirname, filename)
        
        file.save(file_path)
        
        pic = Pic.query.filter(Pic.enregistrement_id == recordID and Pic.nom_table == table_name).first()
        if not pic :
            pic = Pic(
                enregistrement_id=recordID,
                nom_table=table_name,
                nom=filename
            )
            
            db.session.add(pic)
            #db.session.commit()
        else :
            oldName = pic.nom
            old_file_path = os.path.join(table_dirname, oldName)
            
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
                
            pic.nom = filename
        
        db.session.commit()
           
        return table_name +"/"+ pic.nom
         
    except Exception as e:
        raise ExceptionService(e.args[0], 500)
    
    
def save_base_64(tablename, base64_string) :
    output_dir = get_dirname(tablename)
    os.makedirs(output_dir, exist_ok=True)

    # === Fichier de sortie ===
    filename = (generer_chaine_alea(5) + ".jpg").lower()
    image_path = os.path.join(output_dir, filename)

    # === Décodage et sauvegarde ===
    try:
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(base64_string))
            return path_rel_to_url(tablename+"/"+ filename)
        print(f" Image enregistrée avec succès : {image_path}")
    except Exception as e:
        print(f" Erreur lors de la sauvegarde de l'image : {e}")
        raise ExceptionService(str(e), 500)

    
        
    
        