from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.pyd_schemas import ShowCategory, FinType, ShowCategory, AddCategory, UpdateCategory
from app.db.sql_models import User, Category


def add_category(category: AddCategory, db: Session):
    try:
        if get_category_by_name_and_type(category.name, category.finance_type.id, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Category with name: {category.name}  and type {category.finance_type.name} already exist.")
        lobj_category = Category(name=category.name, description=category.description,
                                 finance_type_id=category.finance_type.id)
        db.add(lobj_category)
        db.commit()
        db.refresh(lobj_category)
        if not lobj_category.id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to add category : {lobj_category.name} with type {lobj_category.finance_type.name}")
        return lobj_category
    except Exception as e:
        raise e


def get_category_by_name_and_type(cat_name: str, fin_type_id: int, db: Session):
    return db.query(Category).filter_by(name=cat_name).filter_by(finance_type_id=fin_type_id).first()


def get_category_by_id(cat_id: int, db: Session):
    return db.query(Category).filter_by(id=cat_id).first()


def get_all(db: Session):
    return db.query(Category).all()


def delete_category_by_name_and_type(cat_name: str, fin_type_id: int, db: Session):
    fin_type_object = db.query(FinType).filter_by(id=fin_type_id).first()
    lobj_category = get_category_by_name_and_type(cat_name, fin_type_id, db)
    if not lobj_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with name: {cat_name}  and type {fin_type_object.name} does not exist.")

    lobj_category.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=f"Category with name: {cat_name}  and type {fin_type_object.name} deleted.")


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
                            detail=f"Category with name: {category.name}  and type {category.finance_type.name} does not exist.")

    lobj_category.name = category.name
    lobj_category.description = category.description
    lobj_category.finance_type_id = category.finance_type.id
    db.commit()
    return lobj_category
