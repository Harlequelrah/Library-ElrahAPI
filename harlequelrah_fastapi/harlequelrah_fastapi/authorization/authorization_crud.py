
from sqlalchemy.orm import Session
def has_privilege(db: Session, user, privilege_id):
    roles = user.roles
    for role in roles:
        for p in role.privileges:
            if p.id == privilege_id and p.is_active:
                return True
    else:
        return False
