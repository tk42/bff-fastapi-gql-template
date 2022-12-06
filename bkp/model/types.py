import strawberry
from datetime import datetime
from typing import Optional
from api.model.models import Status, Task

StatusType = strawberry.enum(Status, name="Status")


@strawberry.type(name="Task")
class TaskType:
    task_id: strawberry.ID
    title: str
    description: Optional[str]
    status: StatusType
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_instance(cls, instance: Task) -> "TaskType":
        assert type(instance) is Task, f"instance is {type(instance)}"
        data = instance.__dict__()
        return cls(**data)
