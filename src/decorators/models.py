import json
from models import db


def get_model_name(table_name):
    model_class = next((cls for cls in db.Model.__subclasses__() if cls.__tablename__ == table_name), None)
    return model_class
    
def decorate_model_with_name(normal_name):
    def decorator(cls):
        #print("normal_name")
        cls.normalName = normal_name
        return cls
    return decorator

def decorate_att_unit(attName, unitName):
    def decorator(cls):
        file_path = "schema/units/schema.json"
        with open(file_path) as f:
            jsonDataBrut = json.load(f)
            #print("normal_name")
                
            units = jsonDataBrut["units"]
            #print(units)
            unit = next((unit for unit in units if unit["name"]==unitName), None)
            
            if not unit :
                return
            
            if not hasattr(cls,"__units__") :
                cls.__units__= {}
                
            cls.__units__[attName] = unit
        
        return cls
    return decorator


def decorate_impact_model(table_name, method_name, att_name, impact_model_att_name):
    def decorator(cls):
        file_path = "schema/units/schema.json"
        class_name = get_model_name(table_name)
        if not class_name :
            return None
        
        if not hasattr(class_name, method_name) and callable(getattr(class_name, method_name)) :
            return None
        
        if not hasattr(class_name, impact_model_att_name) :
            return None
        
        
        if not hasattr(cls, att_name) :
            return None
        
        if not hasattr(cls,"__models_impact__") :
            cls.__models_impact__= []
            
        cls.__models_impact__.append(
            {
                "table_name":table_name,
                "method_name":method_name,
                "impact_model_att_name":impact_model_att_name,
                "att_name":att_name
            }
        )
        return cls
    return decorator


def decorate_att_filter_null(att) :
    def decorator(cls):
        if not hasattr(cls,"__filters_null__") :
            cls.__filters_null__= []
            
        cls.__filters_null__.append(
            {
                "att":att
            }
        )       
        
        return cls
    
    return decorator


def decorate_territorable(att) :
    def decorator(cls):
        if not hasattr(cls,"__att_terrirory__") :
            cls.__att_terrirory__= {
                "att":att
            }
        return cls
    
    return decorator
