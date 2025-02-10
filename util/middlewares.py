from fastapi import Request, FastAPI
from typing import Any


class PaginationMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope: dict, receive: Any, send: Any):
        request = Request(scope, receive)

        if request.method == "GET":
            query_params = request.query_params
            page = int(query_params.get("page", 1))
            limit = int(query_params.get("limit", 10))
            offset = (page - 1) * limit

            scope["pagination"] = {"page": page, "limit": limit, "offset": offset}

        await self.app(scope, receive, send)
