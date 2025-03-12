from typing import List, Any, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Profile

class BaseDAO:
    model = None # Устанавливается в дочернем классе

    #Добавить одну запись
    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_instance = cls.model(**values)   #user = User(**user_data)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
    
    #Добавим много записей
    @classmethod
    async def add_many(cls, instances: List[Dict[str, Any]], session: AsyncSession):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances
    