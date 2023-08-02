from sqlalchemy import Column, Integer, VARCHAR, DATE

from .base import BaseModel


class Users(BaseModel):
    __table_name__ = 'users'

    # тг юзер айди
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    last_city = Column(VARCHAR(256), unique=False, nullable=True)

    def __str__(self):
        return f'<User:{self.user_id},{self.last_city}>'

