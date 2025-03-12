from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, ARRAY, text, JSON
from typing import Annotated, List
from sql_enums import GenderEnum, ProfessionEnum, StatusPost, RatingEnum

# Аннотации
uniq_str_an = Annotated[str, mapped_column(unique=True)]
array_or_none_an = Annotated[List[str] | None, mapped_column(JSON)]

class User(Base):
    username:Mapped[uniq_str_an]
    email:Mapped[uniq_str_an]
    password:Mapped[str]
    # profile_id:Mapped[int | None] = mapped_column(ForeignKey('profiles.id'))
    
    #relationship
    # Связь один-ко-многим с Post
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )
    #Связь один-к-одному с Profile
    profile:Mapped["Profile"] = relationship(
        "Profile",
        back_populates='user',
        uselist= False, # Обеспечивает связь один-к-одному
        lazy="joined"
    )
    # Связь один-ко-многим с Comment
    comments:Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="delete, delete-orphan"
    )

class Profile(Base):
    first_name:Mapped[str]
    last_name:Mapped[str | None]
    age:Mapped[int|None]
    gender:Mapped[GenderEnum]
    profession:Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    interests:Mapped[array_or_none_an]
    contacts:Mapped[dict | None] = mapped_column(JSON)
    # Внешний ключ на таблицу users
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    #relationship
    user:Mapped["User"] = relationship(
        "User",
        back_populates='profile',
        uselist = False # Обеспечивает связь один-к-одному
    )

   
class Post(Base):
    title:Mapped[str]
    content:Mapped[str]
    main_photo_url:Mapped[str]
    photos_url:Mapped[array_or_none_an]
    status: Mapped[StatusPost] = mapped_column(default=StatusPost.PUBLISHED, server_default=text("'DRAFT'"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    #relationship
    # Связь многие-к-одному с User
    user:Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )
    comments:Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

class Comment(Base):
    content:Mapped[str]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id:Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published:Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating:Mapped[RatingEnum] = mapped_column(default=RatingEnum.FIVE, server_default=text("'SEVEN'"))

    #relationship
    user:Mapped["User"] = relationship(
        "User",
        back_populates="comments"
        )
    post:Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",

    )
    
    