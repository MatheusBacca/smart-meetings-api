from fastapi import FastAPI

import database.models as models
from database.database import engine
from routes.RoomsWS import rooms_router
from routes.UsersWS import users_router
from routes.ReservationsWS import reservations_router

app = FastAPI()

app.include_router(rooms_router, tags=['Rooms'])
app.include_router(users_router, tags=['Users'])
app.include_router(reservations_router, tags=['Reservarions'])

models.Base.metadata.create_all(bind=engine)
