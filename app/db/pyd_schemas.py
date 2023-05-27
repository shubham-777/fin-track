from datetime import datetime, date
from typing import Union

from pydantic import BaseModel, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email_id: Union[str, None] = None


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email_id: str
    is_active: bool = False


class AddUser(BaseUser):
    password: str


class ShowUser(BaseUser):
    id: int
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at')
    def convert_date_time(cls, param: datetime):
        return param.strftime('%Y-%m-%d, %H:%M:%S')

    class Config:
        orm_mode = True


class UserProfile(BaseUser):
    class Config:
        orm_mode = True


class BaseFinType(BaseModel):
    name: str

    class Config:
        orm_mode = True


class FinType(BaseFinType):
    id: int


class BaseCategory(BaseModel):
    name: str
    description: str


class UpdateCategory(BaseCategory):
    id: int


class ShowCategory(BaseCategory):
    id: int
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at')
    def convert_date_time(cls, param: datetime):
        return param.strftime('%Y-%m-%d, %H:%M:%S')

    class Config:
        orm_mode = True


class BaseTransaction(BaseModel):
    user_id: int
    category_id: int
    finance_type_id: int
    amount: int
    date: date
    title: str
    note: Union[str, None] = None


class UpdateTransaction(BaseTransaction):
    id: int


class ShowTransaction(BaseTransaction):
    id: int
    user_id: int
    category: ShowCategory
    finance_type: FinType
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at')
    def convert_date_time(cls, param: datetime):
        return param.strftime('%Y-%m-%d, %H:%M:%S')

    class Config:
        orm_mode = True
