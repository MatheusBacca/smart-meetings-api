from typing import Optional
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, Field
from database.database import db_dependency
from database.models import Rooms, Reservations, Users
from starlette import status
from datetime import datetime

rooms_router = APIRouter(prefix="/rooms")


class RoomRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="Nome da sala")
    location: str = Field(
        ..., min_length=3, max_length=255, description="Localização da sala"
    )
    capacity: int = Field(
        ..., gt=2, description="Capacidade mínima da sala (deve ser maior que 2)"
    )
    creator_id: int = Field(..., gt=0, description="ID do criador")

    class Config:
        orm_mode = True


@rooms_router.get("/")
async def list_rooms(db: db_dependency):
    return db.query(Rooms).all()


@rooms_router.get("/{id}/availability")
async def check_room_availability(
    db: db_dependency, id: int, start: datetime, end: datetime
):
    room = db.query(Rooms).filter(Rooms.id == id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {id} not found"
        )

    overlapping_reservations = (
        db.query(Reservations)
        .filter(
            Reservations.room_id == id,
            (Reservations.date_time_begin < end) & (Reservations.date_time_end > start),
        )
        .first()
    )

    if overlapping_reservations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available during this time",
        )

    return {"message": "Room is available"}

@rooms_router.get("/{id}/reservations")
async def check_room_reservations(
    db: db_dependency, id: int, date: Optional[datetime] = None
):
    room = db.query(Rooms).filter(Rooms.id == id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {id} not found"
        )

    room_reservations = db.query(Reservations).filter(Reservations.room_id == id)

    if date:
        room_reservations = room_reservations.filter(Reservations.date_time_begin == date).all()

    return room_reservations


@rooms_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(db: db_dependency, room_request: RoomRequest):
    creator = db.query(Users).filter(Users.id == room_request.creator_id).first()
    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {room_request.creator_id} not found",
        )

    room_model = Rooms(**room_request.model_dump())
    db.add(room_model)
    db.commit()
    db.refresh(room_model)

    return {
        "id": room_model.id,
        "name": room_model.name,
        "location": room_model.location,
        "capacity": room_model.capacity,
        "creator_id": room_model.creator_id,
        "created_at": room_model.created_at,
    }
