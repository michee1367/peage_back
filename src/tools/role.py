from flask import current_app

def get_related_roles(role):
    """
    Récupère un rôle donné ainsi que tous les rôles inférieurs hiérarchiquement.
    
    :param role: Le rôle dont on veut récupérer la hiérarchie.
    :return: Une liste contenant le rôle donné et ses sous-rôles.
    """
    hierarchy_roles = current_app.config.get("HIERARCHY_ROLES", {})

    if role not in hierarchy_roles:
        return []

    # Liste des rôles liés, y compris le rôle lui-même
    related_roles = set([role])

    def collect_roles(r):
        """Ajoute récursivement les sous-rôles."""
        for sub_role in hierarchy_roles.get(r, []):
            if sub_role not in related_roles:
                related_roles.add(sub_role)
                collect_roles(sub_role)

    collect_roles(role)

    return list(related_roles)

def get_all_roles() :
    
        hierarchy_roles = current_app.config.get("HIERARCHY_ROLES", {})
        return list(hierarchy_roles.keys())
    