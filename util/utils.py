from logging import Logger
from fastapi import FastAPI, Request
from routes.AuthWS import auth_router
from routes.RootWS import root_router
from routes.RoomsWS import rooms_router
from routes.UsersWS import users_router
from routes.ReservationsWS import reservations_router
from util.logger import setup_logger
from util.middlewares import PaginationMiddleware


def create_app():
    app = FastAPI()

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Receiving request: {request.method} {request.url}.")
        if request_body := await request.body():
            logger.info(f"Request body: {request_body}.")

        response = await call_next(request)

        logger.info(f"Response status code: {response.status_code}.")

        return response

    app.include_router(root_router, tags=["Root"])
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(rooms_router, tags=["Rooms"])
    app.include_router(users_router, tags=["Users"])
    app.include_router(reservations_router, tags=["Reservations"])

    app.add_middleware(PaginationMiddleware)

    logger: Logger = setup_logger(__name__)

    return app
