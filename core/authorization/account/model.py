from core.base.model import BaseModel

from sqlalchemy import Column, String


class Account(BaseModel):
    __tablename__ = 'account'

    account = Column(type_=String(20))
