import uuid
from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict
from bq_schema import BigqueryTable


class Status(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task:
    title: str
    # CAUTION: field 'id' could be overwritten by SurrealDB
    task_id: uuid.UUID = field(default_factory=uuid.uuid4)
    description: Optional[str] = None
    status: Status = Status.TODO
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __dict__(self):
        return {k: str(v) for k, v in asdict(self).items()}


class TaskTable(BigqueryTable):
    name = "tasks"
    schema = Task
