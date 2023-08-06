from typing import List

from sqlalchemy import Integer, VARCHAR, Float, Time, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

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
    updated = mapped_column(Integer, unique=False, nullable=True )
    lat = mapped_column(Float, unique=False, nullable=True)
    lon = mapped_column(Float, unique=False, nullable=True)
    weather: Mapped[List["WeatherStat"]] = relationship()

    def __str__(self):
        return f'<User:{self.city},{self.updated},{self.lat},{self.lon},{self.yandex_weather}>'

    @property
    def to_dict(self) -> dict:
        """
        Конвертирует модель в словарь
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class WeatherStat(Base):
    __tablename__ = 'weather'

    city_name = mapped_column(VARCHAR(32), ForeignKey('cities.city'), unique=True, nullable=False, primary_key=True)
    now = mapped_column(Integer, unique=False, nullable=True)
    feels = mapped_column(Integer, unique=False, nullable=True)
    type_ = mapped_column(VARCHAR(32), unique=False, nullable=True)
    rain = mapped_column(Integer, unique=False, nullable=True)
    ten_days = mapped_column(VARCHAR(256), unique=False, nullable=True)

    @property
    def to_dict(self) -> dict:
        """
        Конвертирует модель в словарь
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


