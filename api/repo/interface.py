from api.model.models import Task


class BaseRepository:
    async def find_by_id(self, id: str) -> Task:
        raise NotImplementedError

    async def find_all(self) -> list[Task]:
        raise NotImplementedError

    async def save(self, task: Task) -> None:
        raise NotImplementedError

    async def delete(self, task: Task) -> None:
        raise NotImplementedError
