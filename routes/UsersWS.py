from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, EmailStr, Field
from starlette import status

from database.models import Users
from database.database import db_dependency


users_router = APIRouter(prefix="/users")


class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="Nome do usuário")
    email: EmailStr = Field(..., description="E-mail do usuário")

    class Config:
        orm_mode = True


@users_router.get("/")
async def list_users(db: db_dependency):
    return db.query(Users).all()


@users_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    user_exisists: bool = (
        db.query(Users).filter(Users.name == user_request.name).first()
    )
    if user_exisists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with name {user_request.name} already exisists",
        )

    user_model = Users(**user_request.model_dump())
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return {
        "id": user_model.id,
        "name": user_model.name,
        "email": user_model.email,
    }
