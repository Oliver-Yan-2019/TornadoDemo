from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy import Column, String

from snowflake.client import get_guid


class_registry = {}
Base = declarative_base(class_registry=class_registry)


class BaseModel(AbstractConcreteBase, Base):
    id = Column(type_=String(19), name="ID", primary_key=True, nullable=False, default=get_guid())

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.id}>'
