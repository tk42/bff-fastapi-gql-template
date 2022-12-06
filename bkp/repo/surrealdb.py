import os
from typing import Union

from api.model.models import Task
from .interface import BaseRepository

from surrealdb.clients.http import HTTPClient

# from surrealdb.common.exceptions import SurrealException

_host: str = os.environ.get("SURREALDB_URL")
_user: str = os.environ.get("SURREALDB_USER")
_pass: str = os.environ.get("SURREALDB_PASS")


# https://github.com/surrealdb/surrealdb.py/blob/main/examples/http_client_example.py


class SurrealDBRepository(BaseRepository):
    def __init__(self, ns: str, db: str):
        self._client = HTTPClient(
            _host,
            namespace=ns,
            database=db,
            username=_user,
            password=_pass,
        )
        self.table = "tasks"

    async def find_by_id(self, task_id: str) -> Union[Task, None]:
        instance = await self._client.select_one(self.table, str(task_id))
        del instance["id"]
        return Task(**instance)

    async def find_all(self) -> list[Task]:
        tasks = []
        for instance in await self._client.select_all(self.table):
            del instance["id"]
            tasks += [Task(**instance)]
        return tasks

    async def save(self, task: Task) -> None:
        await self._client.create_one(self.table, str(task.task_id), task.__dict__())

    async def delete(self, task: Task) -> None:
        await self._client.delete_one(self.table, str(task.task_id))
