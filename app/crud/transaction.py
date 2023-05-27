"""
Author      : Shubham Ahinave
Created at  : 27/05/23
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import date
from db.pyd_schemas import BaseTransaction, UpdateTransaction
from db.sql_models import Transaction


def add_transaction(transaction: BaseTransaction, db: Session):
    try:
        if look_up_for_same_transaction(transaction.title, transaction.user_id, transaction.category_id,
                                        transaction.finance_type_id, transaction.amount, transaction.date, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Transaction name: '{transaction.title}' with other same details already exist.")
        lobj_transaction = Transaction(user_id=transaction.user_id, category_id=transaction.category_id,
                                       finance_type_id=transaction.finance_type_id,
                                       amount=transaction.amount, title=transaction.title, note=transaction.note,
                                       date=transaction.date)
        db.add(lobj_transaction)
        db.commit()
        db.refresh(lobj_transaction)
        if not lobj_transaction.id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to add category : {lobj_transaction.title} for category {lobj_transaction.category.name}")
        return lobj_transaction
    except Exception as e:
        raise e


def update_transaction_by_id(transaction: UpdateTransaction, db: Session):
    lobj_transaction = get_transaction_by_id(transaction.id, db)
    if not lobj_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with id: {transaction.id} does not exist.")

    lobj_transaction.title = transaction.title
    lobj_transaction.user_id = transaction.user_id
    lobj_transaction.category_id = transaction.category_id
    lobj_transaction.finance_type_id = transaction.finance_type_id
    lobj_transaction.amount = transaction.amount
    lobj_transaction.note = transaction.note
    db.commit()
    return lobj_transaction


def get_transaction_by_id(transaction_id: int, db: Session):
    return db.query(Transaction).filter_by(id=transaction_id).first()


def look_up_for_same_transaction(title: str, user_id: int, category_id: int, finance_type_id: int, amount: int,
                                 tran_date: date, db: Session):
    return db.query(Transaction).filter_by(title=title, user_id=user_id, category_id=category_id,
                                           finance_type_id=finance_type_id, amount=amount, date=tran_date).first()


def get_all(db: Session):
    return db.query(Transaction).all()


def delete_transaction_by_id(transaction_id: int, db: Session):
    lobj_transaction = get_transaction_by_id(transaction_id, db)
    if not lobj_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with id: {transaction_id}  does not exist.")

    db.delete(lobj_transaction)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=f"Transaction with id: {transaction_id} deleted.")
