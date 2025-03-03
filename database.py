from sqlalchemy import String, Integer, DateTime, func, ForeignKey, ARRAY, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import settings 
from typing import Annotated, List
from datetime import datetime
import array

DATABASE_URL = settings.get_db_url()

# Анотации 
uniq_str_an = Annotated[str, mapped_column(unique=True)]
content_an = Annotated[str | None, mapped_column(Text)]

# Создаем иснхронный движок для работы с бд
engine = create_async_engine(DATABASE_URL) 
#Создаем фабрику сессий для взаимодейств с бд
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True               # класс абстрактный чтобы не создавать отдельную таблицу под него

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
 
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()+'s'