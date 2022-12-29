from datetime import datetime
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


class ShowFinType(BaseModel):
    name: str

    class Config:
        orm_mode = True


class FinType(ShowFinType):
    id: int


class AddCategory(BaseModel):
    name: str
    description: str
    finance_type: FinType


class UpdateCategory(AddCategory):
    id: int


class ShowCategory(AddCategory):
    id: int
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at')
    def convert_date_time(cls, param: datetime):
        return param.strftime('%Y-%m-%d, %H:%M:%S')

    class Config:
        orm_mode = True
