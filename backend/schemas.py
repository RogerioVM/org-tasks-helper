from datetime import date as Date, datetime
from pydantic import BaseModel


class SessionCreate(BaseModel):
    id: str

class SessionResponse(BaseModel):
    name: str
    lastname: str

class UserCreate(BaseModel):
    name: str
    lastname: str
    age: int
    contact: str

class UserUpdate(BaseModel):
    name: str | None = None
    lastname: str | None = None
    age: int | None = None
    contact: str | None = None

class UserResponse(BaseModel):
    id: str
    name: str
    lastname: str
    age: int
    contact: str

    model_config = {
        "from_attributes": True
    }


class TaskCreate(BaseModel):
    title: str
    difficulty: str
    description: str
    times_per_week: int
    first_date: Date
    date: Date


class TaskUpdate(BaseModel):
    title: str | None = None
    difficulty: str | None = None
    description: str | None = None
    times_per_week: int | None = None
    first_date: Date | None = None
    date: Date | None = None
    
    
class TaskResponse(BaseModel):
    id: str
    title: str
    difficulty: str
    description: str
    times_per_week: int
    first_date: Date
    date: Date
    user_id: str
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
