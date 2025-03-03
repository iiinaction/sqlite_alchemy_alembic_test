from enum import Enum

class GenderEnum(str, Enum):
    MALE = "Мужчина"
    FEMALE = "Женщина"

class ProfessionEnum(str, Enum):
    DEVELOPER = "разработчик"
    DESIGNER = "дизайнер"
    MANAGER = "менеджер"
    TEACHER = "учитель"
    DOCTOR = "врач"
    ENGINEER = "инженер"
    MARKETER = "маркетолог"
    WRITER = "писатель"
    ARTIST = "художник"
    LAWYER = "юрист"
    SCIENTIST = "ученый"
    NURSE = "медсестра"
    UNEMPLOYED = "безработный"    

class StatusPost(str, Enum):
    PUBLISHED = "опубликован"
    DELETED = "удален"
    UNDER_MODERATION = "на модерации"
    DRAFT = "черновик"
    SCHEDULED = "отложенная публикация"

class RatingEnum(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10