from datetime import timedelta, datetime
from typing import Union

from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.db.pyd_schemas import AddUser, TokenData, ShowUser
from app.db.sql import get_session
from app.db.sql_models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "2eed504a80dca24ba07fa02220e03231b62af391d7842767b91c91becb96098f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email_id: str, password: str, db: Session):
    user_obj = get_user(email_id, db)
    if not user_obj:
        return False
    if not verify_password(password, user_obj.hashed_password):
        return False
    return user_obj


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def add_user(user: AddUser, db: Session):
    if get_user(user.email_id, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email_id: {user.email_id} already exits.")
    lobj_user = User(first_name=user.first_name, last_name=user.last_name, email_id=user.email_id,
                     is_active=user.is_active, hashed_password=get_password_hash(user.password))
    db.add(lobj_user)
    db.commit()
    db.refresh(lobj_user)
    if not lobj_user.id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to add user : {user.email_id}")
    return lobj_user


def get_user(email_id: str, db: Session):
    return db.query(User).filter_by(email_id=email_id).first()


def user_login(email_id: str, password: str, db: Session):
    user_bj = authenticate_user(email_id, password, db)
    if not user_bj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"unauthorised user {email_id}")
    user_bj.is_active = True
    db.commit()
    return user_bj


def get_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_id: str = payload.get("sub")
        if email_id is None:
            raise credentials_exception
        token_data = TokenData(email_id=email_id)
    except JWTError:
        raise credentials_exception
    user = get_user(email_id=token_data.email_id)
    if user is None:
        raise credentials_exception
    return user
