import strawberry

from api.resolvers import add_task, delete_task, get_task, get_tasks, update_task
from api.model.types import TaskType


@strawberry.type
class Query:
    task: TaskType = strawberry.field(resolver=get_task)
    tasks: list[TaskType] = strawberry.field(resolver=get_tasks)


@strawberry.type
class Mutation:
    task_add: TaskType = strawberry.field(resolver=add_task)
    task_update: TaskType = strawberry.field(resolver=update_task)
    task_delete: TaskType = strawberry.field(resolver=delete_task)

