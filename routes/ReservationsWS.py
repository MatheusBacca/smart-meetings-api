from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from database.database import db_dependency
from database.models import Reservations

reservations_router = APIRouter(prefix="/reservations")


class ReservationRequest(BaseModel):
    room_id: str = Field(..., gt=0, description="ID da sala a ser reservada")
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


@reservations_router.get("/")
async def list_reservations(db: db_dependency):
    return db.query(Reservations).all()


@reservations_router.post("/")
async def create_reservations(
    db: db_dependency, reservation_request: ReservationRequest
):
    if reservation_request.start_time >= reservation_request.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The start time must be earlier than the end time."
        )

    conflicting_reservation = db.query(Reservations).filter(
        Reservations.room_id == reservation_request.room_id,
        (Reservations.start_time < reservation_request.end_time) & 
        (Reservations.end_time > reservation_request.start_time)
    ).first()

    if conflicting_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The reservation conflicts with an existing reservation."
        )

    reservation_model = Reservations(**reservation_request.model_dump())
    db.add(reservation_model)
    db.commit()
    db.refresh(reservation_model)

    return {
        "id": reservation_model.id,
        "room_id": reservation_model.room_id,
        "user_id": reservation_model.user_id,
        "start_time": reservation_model.start_time,
        "end_time": reservation_model.end_time,
        "created_at": reservation_model.created_at,
    }


@reservations_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(db: db_dependency):
    return db.query(Reservations).all()
