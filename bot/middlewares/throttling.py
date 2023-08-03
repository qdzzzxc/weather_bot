from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        "last_mes": TTLCache(maxsize=10_000, ttl=5),
    }

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in self.caches['last_mes']:
            await event.answer(text='Не спамьте, подождите')
            return
        else:
            self.caches['last_mes'][event.chat.id] = None
        return await handler(event, data)