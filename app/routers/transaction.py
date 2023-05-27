from typing import List

from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from crud.transaction import add_transaction, update_transaction_by_id, get_all, get_transaction_by_id, \
    delete_transaction_by_id
from db.pyd_schemas import ShowTransaction, BaseTransaction, UpdateTransaction
from db.sql import get_session

router = APIRouter(prefix="/transaction", tags=["transaction"], responses={404: {"description": "Not found"}})
tags_metadata = [
    {
        "name": "transaction",
        "description": "User Transactions..",
    }
]


@router.post("/add", response_model=ShowTransaction, status_code=status.HTTP_201_CREATED)
def add_new_transaction(transaction: BaseTransaction, db: Session = Depends(get_session)):
    return add_transaction(transaction, db)


@router.patch("/update", status_code=status.HTTP_201_CREATED, response_model=ShowTransaction)
async def update_transaction(transaction: UpdateTransaction, db: Session = Depends(get_session)):
    return update_transaction_by_id(transaction, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=List[ShowTransaction])
async def get_all_transactions(db: Session = Depends(get_session)):
    return get_all(db)


@router.get("/get/{transaction_id}", status_code=status.HTTP_200_OK, response_model=ShowTransaction)
async def get_for_id(transaction_id: int, db: Session = Depends(get_session)):
    return get_transaction_by_id(transaction_id, db)


@router.delete("/delete/{transaction_id}")
async def delete_by_id(transaction_id: int, db: Session = Depends(get_session)):
    return delete_transaction_by_id(transaction_id, db)
