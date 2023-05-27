from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from crud.fin_type import get_all_types
from db.pyd_schemas import FinType
from db.sql import get_session

router = APIRouter(prefix="/fin_type", tags=["fin_type"], responses={404: {"description": "Not found"}})
tags_metadata = [
    {
        "name": "fin_type",
        "description": "contains all routes related to **Finance Type**",
    }
]


@router.get("/get_all", status_code=status.HTTP_200_OK, response_model=List[FinType])
async def get_all_finance_type(db: Session = Depends(get_session)):
    return get_all_types(db)
