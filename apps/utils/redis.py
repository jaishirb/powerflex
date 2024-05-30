import os
from datetime import timedelta
from typing import Any, Awaitable, Callable, Dict, List, TypeVar

import jsonpickle
import redis
from rq import Queue
from rq.job import Job

from apps.utils import exceptions

T = TypeVar("T")


class RedisHandler:
    def __init__(self) -> None:
        self.host = os.getenv("REDIS_HOST")
        self.instance = redis.Redis(host=self.host)

    async def validate_duplicate(self, *, key: str) -> None:
        if self.instance.get(name=key):
            raise exceptions.KeyAlreadyExistsException(key=key)

    async def set_key(self, *, key: str, value: str) -> None:
        await self.instance.set(name=key, value=value)

    async def add_message_to_stage(self, *, session_id: str, message: str) -> bool:
        abstract_messages = self.instance.get(session_id)
        new_stage = False
        if abstract_messages:
            messages: List[str] = jsonpickle.decode(abstract_messages)
            messages.append(message)
        else:
            messages = [message]
            new_stage = True
        await self.instance.set(
            name=session_id, value=jsonpickle.encode(messages), ex=240
        )
        return new_stage

    async def enqueue_job(
        self,
        *,
        wrapper: Callable[..., None],
        func: Callable[..., Awaitable[None]],
        social_handler: Callable[..., T],
        session_id: str,
        availability: Dict[str, List[Any]],
        secs: int,
    ) -> Job:
        queue = Queue(connection=self.instance)
        response = queue.enqueue_in(
            time_delta=timedelta(seconds=secs),
            session_id=session_id,
            func=wrapper,
            async_func=func,
            availability=availability,
            social_handler_serialized=jsonpickle.encode(social_handler),
            redis_handler_serialized=jsonpickle.encode(self),
        )
        return response

    async def get_message_from_queue(self, *, session_id: str) -> str:
        abstract_messages = self.instance.getdel(session_id)
        if abstract_messages:
            return " ".join(jsonpickle.decode(abstract_messages))
        return ""
