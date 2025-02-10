from datetime import datetime
from pydantic import BaseModel, Field


class ReservationRequest(BaseModel):
    room_id: int = Field(..., gt=0, description="ID da sala a ser reservada")
    start_time: datetime = Field(..., description="Hora de início da reserva")
    end_time: datetime = Field(..., description="Hora de conclusão da reserva")

    class Config:
        from_attributes = True
