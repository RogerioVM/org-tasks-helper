import secrets

from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate, UserUpdate


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    user = User(
        id=secrets.token_hex(4),
        name=user_data.name,
        lastname=user_data.lastname,
        age=user_data.age,
        contact=user_data.contact,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def list_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(
    db: Session,
    user_id: str,
) -> User | None:

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def update_user_service(
    db: Session,
    user: User,
    user_data: UserCreate,
) -> User:

    user.name = user_data.name
    user.lastname = user_data.lastname
    user.age = user_data.age
    user.contact = user_data.contact

    db.commit()
    db.refresh(user)

    return user


def patch_user_service(
    db: Session,
    user: User,
    user_data: UserUpdate,
) -> User:

    changes = user_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in changes.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user_service(
    db: Session,
    user_id: str,
) -> bool:

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True
