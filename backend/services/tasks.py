
from sqlalchemy.orm import Session

from models import Task
from schemas import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
    user_id: str,
) -> Task:

    task = Task(
        title=task_data.title,
        difficulty=task_data.difficulty,
        description=task_data.description,
        times_per_week=task_data.times_per_week,
        first_date=task_data.first_date,
        date=task_data.date,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def list_tasks(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100,
) -> tuple[list[Task], int]:

    query = db.query(Task).filter(Task.user_id == user_id)

    total = query.count()

    tasks = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return tasks, total


def get_task_by_id(
    db: Session,
    task_id: int,
    user_id: str,
) -> Task | None:

    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        .first()
    )


def delete_task(
    db: Session,
    task: Task,
) -> None:

    db.delete(task)
    db.commit()


def update_task(
    db: Session,
    task: Task,
    task_data: TaskCreate,
) -> Task:

    task.title = task_data.title
    task.difficulty = task_data.difficulty
    task.description = task_data.description
    task.times_per_week = task_data.times_per_week
    task.first_date = task_data.first_date
    task.date = task_data.date

    db.commit()
    db.refresh(task)

    return task


def patch_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:

    changes = task_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in changes.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task
