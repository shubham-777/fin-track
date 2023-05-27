from sqlalchemy import Column, Integer, String, func, TIMESTAMP, Boolean, ForeignKey, BigInteger, Date
from sqlalchemy.orm import relationship

from db.sql import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), unique=True)
    last_name = Column(String(20))
    email_id = Column(String(100), unique=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class FinType(Base):
    __tablename__ = "finance_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    finance_type_id = Column(Integer, ForeignKey("finance_type.id"))
    amount = Column(BigInteger, nullable=False)
    title = Column(String(50), nullable=False)
    note = Column(String(255))
    date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship('User', backref='transaction')
    category = relationship('Category', backref='transaction')
    finance_type = relationship("FinType", backref="transaction")
