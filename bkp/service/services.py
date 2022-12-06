from datetime import datetime
from typing import Optional

from api.model.models import Status, Task
from api.repo.inmemory import BaseRepository


class TaskService:
    def __init__(self, repo: type[BaseRepository]) -> None:
        self._repo = repo

    # @property
    # def repo(self) -> type[BaseRepository]:
    #     return self._repo

    async def find(self, id: str) -> Task:
        task = await self._repo.find_by_id(id)

        return task

    async def find_all(self) -> list[Task]:
        tasks = await self._repo.find_all()

        return tasks

    async def create(self, *, title: str, description: Optional[str] = None) -> Task:
        task = Task(title=title, description=description)
        await self._repo.save(task)

        return task

    async def update(self, *, id: str, status: Status) -> Task:
        task = await self._repo.find_by_id(id)
        task.status = status
        task.updated_at = datetime.utcnow()
        await self._repo.save(task)

        return task

    async def delete(self, id: str) -> Task:
        task = await self._repo.find_by_id(id)
        await self._repo.delete(task)

        return task