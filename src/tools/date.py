from datetime import datetime

def parse_date(date_str: str):
    try:
        if not date_str :
            return None 
        # On essaie de parser la date au format attendu
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj
    except ValueError:
        # Si le format est incorrect ou que la date n'existe pas (ex : 2023-23-12)
        return None