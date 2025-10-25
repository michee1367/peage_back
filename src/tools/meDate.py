
from datetime import datetime, timezone

# Fonction pour obtenir la date UTC
def get_utc_now():
    return datetime.now(timezone.utc)