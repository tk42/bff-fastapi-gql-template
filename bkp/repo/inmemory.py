from copy import deepcopy
from typing import Any

from api.model.models import Task
from .interface import BaseRepository

# TODO: async


class InMemoryRepository(BaseRepository):
    _store: dict[str, Any] = {}

    @classmethod
    async def find_by_id(cls, id: str) -> Task:
        task = cls._store.get(id)
        if task is None:
            raise Exception("Not Found")

        return task

    @classmethod
    async def find_all(cls) -> list[Task]:
        tasks = list(cls._store.values())

        return tasks

    @classmethod
    async def save(cls, task: Task) -> None:
        cls._store[str(task.id)] = deepcopy(task)

    @classmethod
    async def delete(cls, task: Task) -> None:
        del cls._store[str(task.id)]
