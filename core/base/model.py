from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.functions import now

from snowflake.client import get_guid
from decimal import Decimal

from environment import environment as env


class_registry = {}
Base = declarative_base(class_registry=class_registry)


class BaseModel(AbstractConcreteBase, Base):
    id = Column(String(19), doc="主键", primary_key=True, nullable=False, default=get_guid())
    create_time = Column(DateTime, doc='创建时间', nullable=False, default=now())
    creator_id = Column(String(19), doc='创建人', nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.id}>'

    @classmethod
    def db(cls):
        return env.db_session

    @property
    def json(self):
        def _get_value(column):
            value = getattr(self, column.name)

            if column.type.__visit_name__ == 'datetime':
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value is not None else None
            elif column.type.__visit_name__ == 'date':
                value = value.strftime('%Y-%m-%d') if value is not None else None
            elif isinstance(value, Decimal):
                value = float(value) if value is not None else None
            else:
                pass

            return value

        columns = self.__table__.columns
        json_ = {str(column.name): _get_value(column) for column in columns}

        return json_
