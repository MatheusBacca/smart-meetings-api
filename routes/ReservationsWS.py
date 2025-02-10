from datetime import date, datetime, timedelta
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Date, cast
from starlette import status
from database.database import db_dependency
from database.models import Reservations, Rooms, Users
from models.ReservationsMO import ReservationRequest
from util.constants import ws_responses
from util.logger import setup_logger

reservations_router = APIRouter(prefix="/reservations")
logger: logging.Logger = setup_logger(__name__)


@reservations_router.get("", responses=ws_responses["reservations_get"])
async def list_reservations(
    db: db_dependency,
    id: Optional[int] = Query(None, description="Filter by reservation ID"),
    room_id: Optional[int] = Query(None, description="Filter by room ID"),
    user_id: Optional[int] = Query(None, description="Filter by user id"),
    date: Optional[date] = Query(
        None, description="Filter by reservations on a specific date"
    ),
    created_at: Optional[date] = Query(
        None, description="Filter by reservations created on a specific date"
    ),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    query = db.query(Reservations)

    if id:
        query = query.filter(Reservations.id == id)
    if room_id:
        query = query.filter(Reservations.room_id == room_id)
    if user_id:
        query = query.filter(Reservations.user_id == user_id)
    if date:
        query = query.filter(cast(Reservations.start_time, Date) == date)
    if created_at:
        query = query.filter(cast(Reservations.created_at, Date) == created_at)

    total_items = query.count()
    reservations = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": (total_items + limit - 1) // limit,
        "reservations": reservations,
    }


@reservations_router.post(
    "", status_code=status.HTTP_201_CREATED, responses=ws_responses["reservations_post"]
)
async def create_reservations(
    db: db_dependency, reservation_request: ReservationRequest
):
    if reservation_request.start_time < datetime.now():
        logger.info("Start time is before current time. Bad request exception raised.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The start time cannot be in the past.",
        )

    if reservation_request.start_time < datetime.now() + timedelta(minutes=30):
        logger.info(
            "Start time is earlier than 30 minutes from now. Bad request exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservations cannot be made within the next 30 minutes.",
        )

    if reservation_request.start_time >= reservation_request.end_time:
        logger.info(
            f"The start time {reservation_request.start_time} is after the end time {reservation_request.end_time}. Bad request exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The start time must be earlier than the end time.",
        )

    room_exists = (
        db.query(Rooms).filter(Rooms.id == reservation_request.room_id).first()
    )
    if room_exists is None:
        logger.info(
            f"Room with id {reservation_request.room_id} does not exist. Not found exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {reservation_request.room_id} does not exist.",
        )

    conflicting_reservation: Optional[Reservations] = (
        db.query(Reservations)
        .filter(
            Reservations.room_id == reservation_request.room_id,
            (Reservations.start_time < reservation_request.end_time)
            & (Reservations.end_time > reservation_request.start_time),
        )
        .first()
    )

    if conflicting_reservation:
        conflicting_reservation_data = {
            "id": conflicting_reservation.id,
            "room_id": conflicting_reservation.room_id,
            "start_time": conflicting_reservation.start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "end_time": conflicting_reservation.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        logger.info(
            f"Reservation conflicts between {reservation_request.start_time} and {reservation_request.end_time} with reservation id {conflicting_reservation.id}."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "The requested reservation conflicts with an existing reservation.",
                "conflicting_reservation": conflicting_reservation_data,
            },
        )

    user_founded = (
        db.query(Users)
        .filter(Users.name.ilike(f"%{reservation_request.user_name}%"))
        .first()
    )
    if not user_founded:
        logger.info(
            f"The user with name {reservation_request.user_name} was not found. Bad request exception raised."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No user named '{reservation_request.user_name}' found.",
        )

    reservation_dict = reservation_request.model_dump()
    reservation_dict.pop("user_name")
    reservation_dict.update({"user_id": user_founded.id})

    reservation_model = Reservations(**reservation_dict)
    db.add(reservation_model)
    db.commit()
    db.refresh(reservation_model)

    logger.info(f"Reservation {reservation_model.id} created successfully.")

    return {
        "id": reservation_model.id,
        "room_id": reservation_model.room_id,
        "user_id": reservation_model.user_id,
        "start_time": reservation_model.start_time,
        "end_time": reservation_model.end_time,
        "created_at": reservation_model.created_at,
    }


@reservations_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ws_responses["reservations_delete"],
)
async def delete_reservation(db: db_dependency, id: int):
    reservation_to_delete = db.query(Reservations).filter(Reservations.id == id).first()

    if reservation_to_delete:
        db.delete(reservation_to_delete)
        db.commit()

        logger.info(f"Reservation {id} deleted.")
    else:
        logger.info(f"Reservation {id} not found.")

    return {}
