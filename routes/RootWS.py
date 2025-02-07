from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to you Start Meetings API!"}
