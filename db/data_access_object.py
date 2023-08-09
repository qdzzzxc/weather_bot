import logging
from typing import NoReturn
from dataclasses import dataclass

from sqlalchemy import select, update, exists
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import (
    NoResultFound,
)

from db.models import Users, Cities, WeatherStat

logger = logging.getLogger(__name__)


class DataAccessObject:
    def __init__(self, session: AsyncSession) -> NoReturn:
        self.session: AsyncSession = session

    #  Get object from id
    async def get_object(
        self, db_object: Users | Cities | WeatherStat, col_val_name, db_object_id: int = None
    ) -> list:
        stmt = select(db_object)
        if db_object_id:
            stmt = stmt.where(getattr(db_object, col_val_name) == db_object_id)

        result = await self.session.execute(stmt)
        return [item.to_dict for item in result.scalars().all()]

    #  Merge object
    async def add_object(
        self,
        db_object: Users | Cities | WeatherStat,
    ) -> None:
        await self.session.merge(db_object)

    async def upd_col_val(self, db_object: Users | Cities | WeatherStat, db_object_id_col, db_object_id: int, col_val_name, value) -> None:
        if db_object_id:
            #под дикт переделать можн
            stmt = update(db_object).where(getattr(db_object, db_object_id_col) == db_object_id).values({col_val_name: value})
            await self.session.execute(stmt)

    async def get_col_val(self, db_object: Users | Cities | WeatherStat, db_object_id_col, db_object_id: int, col_val_name) -> str:
        if db_object_id:
            stmt = select(getattr(db_object, col_val_name)).where(getattr(db_object, db_object_id_col) == db_object_id)
            res = await self.session.execute(stmt)
            return res.scalar()

    async def get_repeat_weather_stat(self, city_name):
        stmt = select(Cities.city, WeatherStat.now, WeatherStat.feels, WeatherStat.type_, WeatherStat.rain,
                      WeatherStat.day_1, WeatherStat.day_2, WeatherStat.day_3, WeatherStat.day_4, WeatherStat.day_5,
                      WeatherStat.day_6, WeatherStat.day_7, WeatherStat.day_8, WeatherStat.day_9,
                      WeatherStat.day_10).join(WeatherStat, Cities.city == WeatherStat.city_name)
        res = await self.session.execute(stmt)
        return res.one().tuple()
