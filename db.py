from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship, Session
from sqlalchemy.ext.declarative import as_declarative, DeclarativeMeta
from sqlalchemy.types import String, Date, BigInteger, Integer, Text
import os

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

class BaseMetaClass(DeclarativeMeta):
    def __init__(cls, name, bases, dict_):
        return super().__init__(name, bases, dict_)
    

@as_declarative(metaclass=BaseMetaClass)
class BaseModel:
    """Base model"""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    def __iter__(self):
        """Iterate over the columns"""
        for column in self.__table__.columns:
            yield column.name, getattr(self, column.name, None)


class NewsModel(BaseModel):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    link: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    published_date: Mapped[date] = mapped_column(Date, nullable=True)
    company_name: Mapped[str] = mapped_column(String, unique=False, nullable=True)


Session = sessionmaker(bind=engine)
current_session = Session()