import logging
from typing import NoReturn, Any, Union
from dataclasses import dataclass

from sqlalchemy import select, update
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import (
    NoResultFound,
)

from db.models import Users

logger = logging.getLogger(__name__)


class DataAccessObject:
    def __init__(self, session: AsyncSession) -> NoReturn:
        self.session: AsyncSession = session

    #  Get object from id
    async def get_object(
        self, db_object: Union[Users], db_object_id: int = None
    ) -> list:
        stmt = select(db_object)
        if db_object_id:
            stmt = stmt.where(db_object.user_id == db_object_id)

        result: ScalarResult = await self.session.execute(stmt)
        return [item.to_dict for item in result.scalars().all()]

    #  Merge object
    async def add_object(
        self,
        db_object: Union[Users],
    ) -> None:
        await self.session.merge(db_object)

    async def add_last_city(self,db_object: Union[Users], db_object_id: int, city_name: str) -> None:
        if db_object_id:
            stmt = update(db_object).where(db_object.user_id == db_object_id).values(last_city = city_name)
        await self.session.execute(stmt)
