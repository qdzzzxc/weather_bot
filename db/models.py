from sqlalchemy import Integer, VARCHAR
from sqlalchemy.orm import mapped_column

from .base import Base


class Users(Base):
    __tablename__ = 'users'

    # тг юзер айди
    user_id = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    last_city = mapped_column(VARCHAR(256), unique=False, nullable=True)

    def __str__(self):
        return f'<User:{self.user_id},{self.last_city}>'

    @property
    def to_dict(self) -> dict:
        """
        Конвертирует модель в словарь
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

