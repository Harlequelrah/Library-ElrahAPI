from fastapi.responses import JSONResponse
from sqlalchemy import func
from harlequelrah_fastapi.authorization.privilege.privilege_model import Privilege, PrivilegeCreateModel, PrivilegeUpdateModel
from harlequelrah_fastapi.utility.utils import update_entity
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, status


async def get_count_privileges(db: Session):
    return db.query(func.count((Privilege.id))).scalar()


async def create_privilege(db: Session, privilege_create: PrivilegeCreateModel):
    new_privilege = Privilege(**privilege_create)
    try:
        db.add(new_privilege)
        db.commit()
        db.refresh(new_privilege)
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error during creating privilege , details : {str(e)}",
        )
    return new_privilege


async def get_privilege(db: Session, privilege_id: int):
    privilege = db.query(Privilege).filter(Privilege.id == privilege_id).first()
    if not privilege:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Privilege {privilege_id} not found "
        )
    return privilege


async def get_privileges(db: Session, skip: int = 0, limit: int = None):
    if limit is None:
        limit = await get_count_privileges(db)
    privileges = db.query(Privilege).skip(skip).offset(limit).all()
    if not privileges:
        raise HE(status_code=status.HTTP_404_NOT_FOUND, detail=f"Any privileges found")
    return privileges


async def update_privilege(db: Session, privilege_id: int, privilege_update: PrivilegeUpdateModel):
    existingPrivilege = await get_privilege(db, privilege_id)
    existingPrivilege = update_entity(existingPrivilege, privilege_update)
    try:
        db.commit()
        db.refresh(existingPrivilege)
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error during updating privilege {privilege_id}, details : {str(e)}",
        )
    return existingPrivilege


async def delete_privilege(db: Session, privilege_id: int):
    existingPrivilege = await get_privilege(db, privilege_id)
    try:
        db.delete(existingPrivilege)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Privilege deleted successfully"},
        )
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during deleting privilege {privilege_id}, details : {str(e)}",
        )


async def add_privilege_to_user(self, db: Session, user, privilege_id):
    privilege = await get_privilege(db, privilege_id)
    user.privileges.append(privilege)
    try:
        db.commit()
        db.refresh(user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Privilege added successfully"},
        )
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding privilege to user {user.id}, details : {str(e)}",
        )


async def has_privilege(db: Session, user, privilege_id):
    roles = user.roles
    for role in roles:
        for p in role.privileges:
            if p.id == privilege_id and p.is_active:
                return True
    else:
        return False
