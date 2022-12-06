from enum import Enum
from typing import Optional
from datetime import datetime
from api.repo.postgres.db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass, field, asdict


class Status(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task(Base, BaseModel):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    description: Optional[str] = None
    status: Status = Status.TODO
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __dict__(self):
        return {k: str(v) for k, v in asdict(self).items()}

    class Config:
        orm_mode = True


class TaskCreate(Task):
    pass
