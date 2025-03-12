from dao.dao import UserDAO
from database import connection
from asyncio import run
from schemas import ProfilePydantic, UserPydantic

@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)

#Преобразуем результат поиска по ID в питоновский словарь через Pydantic-схему
@connection
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.get_user_info(session=session, user_id=user_id)
    if rez:
        return UserPydantic.model_validate(rez).model_dump()
    return {'message':f'Пользовтаель с ID:{user_id} не найден!'}

# all_users = run(select_all_users())
# for i in all_users:
#     user_pydantic = UserPydantic.model_validate(i)
#     print(user_pydantic.model_dump())

info = run(select_full_user_info(user_id=1))
print(info)