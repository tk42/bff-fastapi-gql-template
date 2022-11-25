from api.model.models import Task

class BaseRepository:
    async def find_by_id(id: str) -> Task:
        raise NotImplementedError
    async def find_all() -> list[Task]:
        raise NotImplementedError
    async def save(task: Task) -> None:
        raise NotImplementedError
    async def delete(task: Task) -> None:
        raise NotImplementedError
