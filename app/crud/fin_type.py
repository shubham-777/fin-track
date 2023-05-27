from sqlalchemy.orm import Session

from db.sql_models import FinType


def get_all_types(db: Session):
    return db.query(FinType).all()
