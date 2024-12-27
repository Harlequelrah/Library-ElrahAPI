from fastapi.responses import JSONResponse
from sqlalchemy import func
from harlequelrah_fastapi.authorization.role.role_model import Role, RoleCreateModel, RoleUpdateModel
from harlequelrah_fastapi.utility.utils import update_entity
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, status


async def get_count_roles(db: Session):
    return db.query(func.count((Role.id))).scalar()


async def create_role(db: Session, role_create: RoleCreateModel):
    new_role = Role(**role_create)
    try:
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error during creating role , details : {str(e)}",
        )
    return new_role


async def get_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role_id} not found "
        )
    return role


async def get_roles(db: Session, skip: int = 0, limit: int = None):
    if limit is None:
        limit = await get_count_roles(db)
    return db.query(Role).skip(skip).offset(limit).all()


async def update_role(db: Session, role_id: int, role_update: RoleUpdateModel):
    existingRole = await get_role(db, role_id)
    existingRole = update_entity(existingRole, role_update)
    try:
        db.commit()
        db.refresh(existingRole)
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error during updating role {role_id}, details : {str(e)}",
        )
    return existingRole


async def delete_role(db: Session, role_id: int):
    existingRole = await get_role(db, role_id)
    try:
        db.delete(existingRole)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Role deleted successfully"},
        )
    except HE as e:
        db.rollback()
        raise HE(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during deleting role {role_id}, details : {str(e)}",
        )

async def add_role_to_user(db:Session,user,role_id):
    role = await get_role(db, role_id)
    user.roles.append(role)
    try:
        db.commit()
        db.refresh(user)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Role added successfully"})
    except HE as e:
        db.rollback()
        raise HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding role to user {user.id}, details : {str(e)}")
