from sqlalchemy.ext.asyncio import AsyncSession
from api.model.models import task as task_model

# from api.model.schema import task as task_schema
from sqlalchemy import select


async def get_tasks(db: AsyncSession):
    result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
            )
        )
    )
    return result.all()


async def get_task(db: AsyncSession, task_id):
    result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
            ).filter(task_model.Task.id == task_id)
        )
    )
    return result.first()


async def create_task(db: AsyncSession, task_create: task_model.TaskCreate):
    task = task_model.Task(
        title=task_create.title,
        description=task_create.description,
        status=task_create.status,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession, task_id, task_create: task_model.TaskCreate):
    result = await (db.execute(select(task_model.Task).filter(task_model.Task.id == task_id)))
    task = result.first()
    task[0].title = task_create.title
    task[0].description = task_create.description
    task[0].status = task_create.status
    db.add(task[0])
    await db.commit()
    await db.refresh(task[0])
    return task[0]


async def delete_task(db: AsyncSession, task_id):
    result = await db.execute(select(task_model.Task).filter(task_model.Task.id == task_id))
    task = result.first()
    await db.delete(task[0])
    await db.commit()
    return task
