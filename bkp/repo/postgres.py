from typing import Union
from api.model.models import Task
from api.model.schema import TaskCreate
from .interface import BaseRepository
from api.repo.postgres.db import get_db
from api.repo.postgres.operation import get_tasks, get_task, create_task, delete_task


class PostgresDBRepository(BaseRepository):
    async def __init__(self, ns: str, db: str):
        pass

    async def find_by_id(self, task_id: str) -> Union[Task, None]:
        result = await get_task(await get_db(), task_id)
        return Task(**result)

    async def find_all(self) -> list[Task]:
        result = await get_tasks(await get_db())
        return [Task(**task) for task in result]

    async def save(self, task: Task) -> None:
        task_create = TaskCreate(
            title=task.title,
            description=task.description,
            status=task.status,
        )
        return await create_task(await get_db(), task_create)

    async def delete(self, task: Task) -> None:
        return await delete_task(await get_db(), task.task_id)
