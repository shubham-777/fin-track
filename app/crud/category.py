from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.pyd_schemas import FinType, BaseCategory, UpdateCategory
from db.sql_models import Category


def add_category(category: BaseCategory, db: Session):
    try:
        if get_category_by_name(category.name, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Category with name: {category.name}  and type {category.finance_type.name} already exist.")
        lobj_category = Category(name=category.name, description=category.description)
        db.add(lobj_category)
        db.commit()
        db.refresh(lobj_category)
        if not lobj_category.id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to add category : {lobj_category.name} with type {lobj_category.finance_type.name}")
        return lobj_category
    except Exception as e:
        raise e


def get_category_by_name(cat_name: str, db: Session):
    return db.query(Category).filter_by(name=cat_name).first()


def get_category_by_id(cat_id: int, db: Session):
    return db.query(Category).filter_by(id=cat_id).first()


def get_all(db: Session):
    return db.query(Category).all()


def delete_category_by_name_and_type(cat_name: str,  db: Session):
    lobj_category = get_category_by_name(cat_name, db)
    if not lobj_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with name: {cat_name}  does not exist.")

    lobj_category.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=f"Category with name: {cat_name} deleted.")


def delete_category_by_id(cat_id: int, db: Session):
    lobj_category = get_category_by_id(cat_id, db)
    if not lobj_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {cat_id}  does not exist.")

    db.delete(lobj_category)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=f"Category with id: {cat_id} deleted.")


def update_category_by_id(category: UpdateCategory, db: Session):
    lobj_category = get_category_by_id(category.id, db)
    if not lobj_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {category.id} does not exist.")

    lobj_category.name = category.name
    lobj_category.description = category.description
    db.commit()
    return lobj_category
