from sqlalchemy import Integer, VARCHAR, Float, Time
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

class Cities(Base):
    __tablename__ = 'cities'

    city = mapped_column(VARCHAR(32), unique=True, nullable=False, primary_key=True)
    updated = mapped_column(Time, unique=False, nullable=True )
    lat = mapped_column(Float, unique=False, nullable=True)
    lon = mapped_column(Float, unique=False, nullable=True)
    open_weather_key = mapped_column(VARCHAR(256), unique=False, nullable=True)
    yandex_weather_key = mapped_column(VARCHAR(256), unique=False, nullable=True)

    def __str__(self):
        return f'<User:{self.city},{self.updated},{self.lat},{self.lon},{self.yandex_weather}>'

    @property
    def to_dict(self) -> dict:
        """
        Конвертирует модель в словарь
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

