from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, Response, status, Depends
from settings.database  import authentication
from sqlalchemy import or_
from harlequelrah_fastapi.utility.utils import update_entity

User = authentication.User
UserLoginModel = authentication.User
UserCreate = authentication.UserCreateModel
UserUpdate = authentication.UserUpdateModel
dependencies = [Depends(authentication.get_session), Depends(authentication.get_current_user)]
async def get_count_users(db:Session=dependencies[0]):
    return db.query(func.count(User.id)).scalar()


async def is_unique(sub: str, db:Session=dependencies[0]):
    user = db.query(User).filter(or_(User.email == sub, User.username == sub)).first()
    return user is None


async def create_user(
    user: UserCreate,
    db: Session = dependencies[0],
    access_token: str = dependencies[1],
):
    new_user = User(**user.dict())
    if not is_unique(db, new_user.email) or not is_unique(db, new_user.username):
        raise HE(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom d'utilisateur ou l'email existe déjà",
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user(access_token: str = dependencies[1], db: Session = dependencies[0], id: int = None, sub: str = None):
    user = (
        db.query(User)
        .filter(or_(User.username == sub, User.email == sub, User.id == id))
        .first()
    )
    return user


async def get_users(
    access_token: str = dependencies[1],
    db: Session = dependencies[0],
    skip: int = 0,
    limit: int = None,
):
    limit = await get_count_users(db)
    users = db.query(User).offset(skip).limit(limit).all()
    return users


async def update_user(
    user_id: int,
    user: UserUpdate,
    access_token: str = dependencies[1],
    db: Session = dependencies[0],
):
    existing_user = await get_user(db, user_id)
    update_entity(existing_user, user)
    db.commit()
    db.refresh(existing_user)
    return existing_user
