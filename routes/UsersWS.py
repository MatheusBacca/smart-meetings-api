import logging
from typing import Optional
from fastapi import HTTPException, APIRouter, Query
from starlette import status

from database.models import Users
from database.database import db_dependency
from models.UsersMO import UserRequest
from util.constants import ws_responses
from util.logger import setup_logger

users_router = APIRouter(prefix="/users")

logger: logging.Logger = setup_logger(__name__)


@users_router.get("", responses=ws_responses["users_get"])
async def list_users(
    db: db_dependency,
    id: Optional[int] = Query(None, description="Filter by user ID"),
    name: Optional[str] = Query(None, description="Filter by user name"),
    email: Optional[str] = Query(None, description="Filter by user email"),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, le=100, description="Number of items per page, max 100"),
):
    query = db.query(Users)

    if id:
        query = query.filter(Users.id == id)
    if name:
        query = query.filter(Users.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Users.email.ilike(f"%{email}%"))

    total_items = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": (total_items + limit - 1) // limit,
        "users": users,
    }


@users_router.post(
    "", status_code=status.HTTP_201_CREATED, responses=ws_responses["users_post"]
)
async def create_user(db: db_dependency, user_request: UserRequest):
    user_exisists: Optional[Users] = (
        db.query(Users).filter(Users.name == user_request.name).first()
    )

    if user_exisists:
        logger.info(
            f"Conflict: User name '{user_request.name}' already exists. Conflict exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with name '{user_request.name}' already exists.",
        )

    email_exisists: Optional[Users] = (
        db.query(Users).filter(Users.email == user_request.email).first()
    )

    if email_exisists:
        logger.info(
            f"Conflict: User email '{user_request.email} already exists. Conflict exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user_request.email}' is already registered for another user.",
        )

    user_model = Users(**user_request.model_dump())
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    logger.info(f"User {user_model.id} was created successfully.")

    return {
        "id": user_model.id,
        "name": user_model.name,
        "email": user_model.email,
    }
