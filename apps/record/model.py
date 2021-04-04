from sqlalchemy import Column, Text, String

from core.base.model import BaseModel


class Record(BaseModel):
    __tablename__ = 'record'

    content = Column(Text, doc='日志内容', nullable=False)
    image_index = Column(String(1048), doc='照片', nullable=False)
