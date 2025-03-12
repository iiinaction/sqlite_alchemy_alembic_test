from sqlalchemy import String, Integer, DateTime, func, ForeignKey, ARRAY, Text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, class_mapper
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import settings 
from typing import Annotated, List
from datetime import datetime

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

    def to_dict(self) -> dict:
        """Универсальный метод для конвертаици объекта SQLAlchemy в словарь"""
        #получаем маппер для текущего объекта
        columns = class_mapper(self.__class__).columns
        #возвращаем словарь все колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns} 
    
    

    
# Декоратор для создания сессии
def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper

# @connection
# async def get_users(session):
#     return await session.execute(select(User))