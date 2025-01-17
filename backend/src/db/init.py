from datetime import datetime
from typing import ClassVar

from pydantic.v1 import validator
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

import config

engine = create_engine('sqlite:///' + config.DB_PATH)
Base = declarative_base()


class Alert(Base):
    date_format: ClassVar[str] = "%d.%m.%Y"
    __tablename__ = 'alert'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String)
    dt = Column(DateTime)
    type = Column(String)

    @validator("dt", pre=True)
    def string_to_date(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, cls.date_format).date()
        return v


class Stat(Base):
    date_format: ClassVar[str] = "%d.%m.%Y"
    __tablename__ = 'stat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    dt = Column(DateTime)
    count = Column(Integer)

    @validator("dt", pre=True)
    def string_to_date(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, cls.date_format).date()
        return v