from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, Response, status, Depends
from settings.database  import get_db
from settings.secret import authentication
from sqlalchemy import or_
from harlequelrah_fastapi.utility.utils import update_entity

User = authentication.User
UserLoginModel = authentication.User
UserCreate = authentication.UserCreateModel
UserUpdate = authentication.UserUpdateModel

async def get_count_users(db: Session):
    return db.query(func.count(User.id)).scalar()


async def is_unique(sub: str, db: Session):
    user = db.query(User).filter(or_(User.email == sub, User.username == sub)).first()
    return user is None


async def create_user(user: UserCreate, db: Session):
    new_user = User(**user.dict())
    if not is_unique(db, new_user.email) or not is_unique(db, new_user.username):
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom d'utilisateur ou l'email existe déjà",
        )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HE(
            status_code=500,
            detail=f"Erreur lors de la creation de l'utilisateur : {str(e)}",
        )
    return new_user


async def get_user(db: Session, id: int = None, sub: str = None):
    user = (
        db.query(User)
        .filter(or_(User.username == sub, User.email == sub, User.id == id))
        .first()
    )
    if not user:
        raise HE(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur Non Trouvé")
    else:
        return user


async def get_users(db: Session, skip: int = 0, limit: int = None):
    limit = await get_count_users(db)
    users = db.query(User).offset(skip).limit(limit).all()
    if not users:
        raise HE(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucun utilisateur trouvé"
        )
    else:
        return users





async def update_user(user_id: int, user: UserUpdate, db: Session):
    existing_user = await get_user(db, user_id)
    try:
        update_entity(existing_user, user)
        db.commit()
        db.refresh(existing_user)
    except HE as e:
        db.rollback()
        raise HE(
            status_code=500,
            detail=f"Erreur lors de la mise à jour de l'utilisateur : {str(e)}",
        )
    return existing_user
