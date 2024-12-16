from harlequelrah_fastapi.authorization.role_model import Role , RoleCreate, RoleUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE,status

async def create_role(db:Session,role_create:RoleCreate):
    new_role=Role(**role_create)
    try :
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
    except HE as e :
        db.rollback()
        raise HE(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error during creating role , details : {e.detail}")
    return new_role

async def get_role(db:Session,role_id:int):
    role=db.query(Role).filter(Role.id==role_id).first()
    if not role : raise HE(status_code=status.HTTP_404_NOT_FOUND,detail=f"Role {role_id} not found ")
    return role
