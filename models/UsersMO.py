from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Gera o hash da senha usando Bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="User name.")
    password: str = Field(
        ..., min_length=8, max_length=255, description="User password."
    )
    email: EmailStr = Field(..., description="User email.")

    class Config:
        from_attributes = True
