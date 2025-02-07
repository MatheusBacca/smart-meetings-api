from typing import Optional
from fastapi import HTTPException, APIRouter, Query
from sqlalchemy import Date, cast
import logging
from database.database import db_dependency
from database.models import Rooms, Reservations
from starlette import status
from datetime import date, datetime
from util.constants import ws_responses

from models.RoomsMO import RoomsPostRequest
from util.logger import setup_logger

rooms_router = APIRouter(prefix="/rooms")
logger: logging.Logger = setup_logger(__name__)


@rooms_router.get("", responses=ws_responses["rooms_get"])
async def list_rooms(
    db: db_dependency,
    id: Optional[int] = Query(None, description="Filter by user ID"),
    name: Optional[str] = Query(None, description="Filter by user name"),
    location: Optional[str] = Query(None, description="Filter by room location"),
    capacity: Optional[int] = Query(None, description="Filter by room capacity"),
    creator_id: Optional[int] = Query(
        None, description="Filter by rooms created by a specific user"
    ),
    created_at: Optional[date] = Query(
        None, description="Filter by rooms created on a specific date"
    ),
):
    query = db.query(Rooms)

    if id:
        query = query.filter(Rooms.id == id)
    if name:
        query = query.filter(Rooms.name.ilike(f"%{name}%"))
    if location:
        query = query.filter(Rooms.location.ilike(f"%{location}%"))
    if capacity:
        query = query.filter(Rooms.capacity == capacity)
    if creator_id:
        query = query.filter(Rooms.creator_id == creator_id)
    if created_at:
        query = query.filter(cast(Rooms.created_at, Date) == created_at)

    return {"rooms": query.all()}


@rooms_router.get(
    "/{id}/availability", responses=ws_responses["rooms_get_availability"]
)
async def check_room_availability(
    db: db_dependency,
    id: int,
    start: datetime = Query(..., description="Start datetime for the reservation"),
    end: datetime = Query(..., description="End datetime for the reservation"),
):
    if start >= end:
        logger.info(
            f"The start time {start} is after the end time {end}. Bad request exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The start time must be earlier than the end time.",
        )

    room = db.query(Rooms).filter(Rooms.id == id).first()
    if not room:
        logger.info(f"No room with id {id} founded. Not found exception raised")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {id} not found"
        )

    overlapping_reservation: Optional[Reservations] = (
        db.query(Reservations)
        .filter(
            Reservations.room_id == id,
            (Reservations.start_time >= end) & (Reservations.end_time <= start),
        )
        .first()
    )

    is_available: bool = True
    if overlapping_reservation is not None:
        is_available: bool = False

    return {"room_id": id, "availability": is_available}


@rooms_router.get(
    "/{id}/reservations", responses=ws_responses["rooms_get_reservations"]
)
async def check_room_reservations(
    db: db_dependency, id: int, date: Optional[date] = None
):
    room = db.query(Rooms).filter(Rooms.id == id).first()
    if not room:
        logger.info(f"No room with id {id} founded. Not found exception raised")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id '{id}' not found.",
        )

    room_reservations = db.query(Reservations).filter(Reservations.room_id == id)

    if date is not None:
        room_reservations = room_reservations.filter(
            cast(Reservations.start_time, Date) == date
        )

    return {"reservations": room_reservations.all()}


@rooms_router.post(
    "", status_code=status.HTTP_201_CREATED, responses=ws_responses["rooms_post"]
)
async def create_room(
    db: db_dependency,
    room_request: RoomsPostRequest,
):
    room_model = Rooms(**room_request.model_dump())
    db.add(room_model)
    db.commit()
    db.refresh(room_model)

    logger.info(f"Room {room_model.id} was created successfully.")

    return {
        "id": room_model.id,
        "name": room_model.name,
        "location": room_model.location,
        "capacity": room_model.capacity,
        "creator_id": room_model.creator_id,
        "created_at": room_model.created_at,
    }
