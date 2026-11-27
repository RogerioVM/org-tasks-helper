from fastapi import Depends, FastAPI, Header, HTTPException, Query, Response
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User
from schemas import (
    SessionCreate,
    SessionResponse,
    UserCreate,
    UserUpdate,
    UserResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)

from services.tasks import (
    create_task,
    delete_task as delete_task_service,
    get_task_by_id,
    list_tasks,
    update_task as update_task_service,
    patch_task as patch_task_service,
)

from services.users import (
    create_user as create_user_service,
    get_user_by_id,
    list_users,
    update_user_service,
    patch_user_service,
    delete_user_service
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

###################### Handles User ######################

def get_current_user(
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
) -> User:

    user = get_user_by_id(db, x_user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user",
        )

    return user


@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    new_user = create_user_service(db, user)

    return {
        "id": new_user.id
    }


@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
):
    return list_users(db)


@app.put("/user/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = get_user_by_id(
        db=db,
        user_id=current_user.id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return update_user_service(
        db=db,
        user=user,
        user_data=user_data,
    )


@app.patch("/user/{user_id}", response_model=UserResponse)
def patch_user_endpoint(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    changes = user_data.model_dump(
        exclude_unset=True,
    )

    if not changes:
        raise HTTPException(
            status_code=422,
            detail="At least one field must be provided",
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null",
        )

    user = get_user_by_id(
        db=db,
        user_id=current_user.id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return patch_user_service(
        db=db,
        user=user,
        user_data=user_data,
    )

@app.delete("/users/{user_id}", status_code=204)
def delete_user( user_id: str, db: Session = Depends(get_db)):
    deleted = delete_user_service(
        db=db,
        user_id=user_id,
    )
       
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )


###################### Handles Session ######################

@app.post("/sessions", response_model=SessionResponse)
def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
):

    user = get_user_by_id(
        db,
        session_data.id,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail=(
                "No user with this ID, "
                "please try again or make an account"
            ),
        )

    return user


###################### Handles Tasks ######################

@app.post("/tasks", response_model=TaskResponse)
def create_task_endpoint(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(
        db=db,
        task_data=task_data,
        user_id=current_user.id,
    )

@app.get("/tasks", response_model=list[TaskResponse])

def get_tasks(
    response: Response,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    tasks, total = list_tasks(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )

    response.headers["X-Total-Count"] = str(total)

    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return update_task_service(
        db=db,
        task=task,
        task_data=task_data,
    )
    
@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def patch_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    changes = task_data.model_dump(
        exclude_unset=True,
    )

    if not changes:
        raise HTTPException(
            status_code=422,
            detail="At least one field must be provided",
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null",
        )

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return patch_task_service(
        db=db,
        task=task,
        task_data=task_data,
    )

@app.delete(
    "/tasks/{task_id}",
    status_code=204,
)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    delete_task_service(
        db=db,
        task=task,
    )