from functools import reduce

def get_attr_by_path(obj, attr_path):
    """Permet d'accéder à un attribut imbriqué à partir d'une chaîne 'a.b.c'"""
    try:
        return reduce(getattr, attr_path.split('.'), obj)
    except AttributeError:
        
        return None