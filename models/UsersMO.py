from pydantic import BaseModel, EmailStr, Field


class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="User name.")
    email: EmailStr = Field(..., description="User email.")

    class Config:
        orm_mode = True
