from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.crud.user import add_user, get_user as get_user_crud, user_login
from app.db.pyd_schemas import AddUser, ShowUser
from app.db.sql import get_session

router = APIRouter(prefix="/user", tags=["user"], responses={404: {"description": "Not found"}})
tags_metadata = [
    {
        "name": "user",
        "description": "contains all routes related to **users**",
    }
]


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def add(user: AddUser, db: Session = Depends(get_session)):
    return add_user(user, db)


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def login(mail_id: str, password: str, db: Session = Depends(get_session)):
    return user_login(mail_id, password, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get_by_email_id(email_id: str = 'test@mail.com', db: Session = Depends(get_session)):
    return get_user_crud(email_id, db)
