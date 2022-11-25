import strawberry

from api.model.inputs import AddTaskInput, UpdateTaskInput
from api.repo.surrealdb import SurrealDBRepository
from api.service.services import TaskService
from api.model.types import TaskType

db = SurrealDBRepository("tasks", "tasks")


async def get_task(id: strawberry.ID) -> TaskType:
    service = TaskService(db)
    task = await service.find(id)

    return TaskType.from_instance(task)


async def get_tasks() -> list[TaskType]:
    service = TaskService(db)
    tasks = await service.find_all()

    return [TaskType.from_instance(task) for task in tasks]


async def add_task(task_input: AddTaskInput) -> TaskType:
    service = TaskService(db)
    task = await service.create(**task_input.__dict__)

    return TaskType.from_instance(task)


async def update_task(task_input: UpdateTaskInput) -> TaskType:
    service = TaskService(db)
    task = await service.update(**task_input.__dict__)

    return TaskType.from_instance(task)


async def delete_task(id: strawberry.ID) -> TaskType:
    service = TaskService(db)
    task = await service.delete(id)

    return TaskType.from_instance(task)