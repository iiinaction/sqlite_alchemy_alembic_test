from database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Profile
from asyncio import run
from sql_enums import GenderEnum, ProfessionEnum, StatusPost, RatingEnum


# метод с несвязанными таблица one to one
@connection
async def create_user_example(username:str, email:str, password:str, session: AsyncSession ) -> int: 
    # возвращает индикатор созданного пользователя
    user = User(username = username, email = email, password= password)
    session.add(user)
    await session.commit()
    
# new_user_id = run(create_user_example(username='Alexander', 
#                                       email='andbuffer@gmail.com',
#                                       password='qwerty12345'))

# print(f'Новый пользователь с id:{new_user_id} создан!')

#метод flush для двух связанных таблиц
@connection
async def get_user_by_id_example_3(username:str, email:str, password:str,
                                   first_name:str,
                                   last_name:str | None,
                                   age:int | None,
                                   gender: GenderEnum | None,
                                   proffesion: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession)-> dict[str, int]:
    try: 
        user = User(username = username, email = email, password= password)
        session.add(user)
        await session.flush()

        profile = Profile(
            user_id = user.id,
            first_name = first_name,
            last_name = last_name,
            age = age,
            gender = gender,
            proffesion = proffesion,
            interests = interests,
            contacts = contacts
        )
        session.add(profile)
        
        #Одина коммит для обоих
        await session.commit()
        print(f'Пользователь создани с id:{user.id}, ему присвоен профиль с id:{profile.id}')
        return {'user_id':user.id,'profile_id':profile.id}
    except Exception as e:
        await session.rollback() # Откат транзакции при ошибке
        raise e

@connection
async def create_user_example_4(users_data:list[dict], session:AsyncSession) ->list[int]:
    """
    Создает нескольких пользователей с использованием ORM SQLAlchemy.

    Аргументы:
    - users_data: list[dict] - список словарей, содержащих данные пользователей
      Каждый словарь должен содержать ключи: 'username', 'email', 'password'.
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - list[int] - список идентификаторов созданных пользователей
    """
    users_list = [
        User(
            username = user_data['username'],
            email = user_data['email'],
            password = user_data['password']
        )
        for user_data in users_data
    ]
    session.add_all(users_list)
    await session.commit()
    return [user.id for user in users_list]

users = [
    {"username": "michael_brown", "email": "michael.brown@example.com", "password": "pass1234"},
    {"username": "sarah_wilson", "email": "sarah.wilson@example.com", "password": "mysecurepwd"},
    {"username": "david_clark", "email": "david.clark@example.com", "password": "davidsafe123"},
    {"username": "emma_walker", "email": "emma.walker@example.com", "password": "walker987"},
    {"username": "james_martin", "email": "james.martin@example.com", "password": "martinpass001"}
]

# run(create_user_example_4(users_data=users))
