from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.crud.category import add_category, update_category_by_id, get_all as crud_get_all, delete_category_by_id, \
    get_category_by_id
from app.db.pyd_schemas import AddUser, ShowUser, ShowCategory, ShowCategory, AddCategory, UpdateCategory
from app.db.sql import get_session

router = APIRouter(prefix="/category", tags=["category"], responses={404: {"description": "Not found"}})
tags_metadata = [
    {
        "name": "category",
        "description": "contains all routes related to **financial categories**",
    }
]


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=ShowCategory)
def add_new_category(category: AddCategory, db: Session = Depends(get_session)):
    return add_category(category, db)


@router.patch("/update", status_code=status.HTTP_201_CREATED, response_model=ShowCategory)
async def update_category(category: UpdateCategory, db: Session = Depends(get_session)):
    return update_category_by_id(category, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=List[ShowCategory])
async def get_all_category(db: Session = Depends(get_session)):
    return crud_get_all(db)


@router.get("/get/{category_id}", status_code=status.HTTP_200_OK, response_model=ShowCategory)
async def get_for_id(category_id: int, db: Session = Depends(get_session)):
    return get_category_by_id(category_id, db)


@router.delete("/delete/{category_id}")
async def delete_by_id(category_id: int, db: Session = Depends(get_session)):
    return delete_category_by_id(category_id, db)
