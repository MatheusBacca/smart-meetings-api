from datetime import datetime
from pydantic import BaseModel, Field


class ReservationRequest(BaseModel):
    room_id: int = Field(..., gt=0, description="ID da sala a ser reservada")
    user_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nome do usuário que está reservando a sala",
    )
    start_time: datetime = Field(..., description="Hora de início da reserva")
    end_time: datetime = Field(..., description="Hora de conclusão da reserva")

    class Config:
        orm_mode = True
