from contextlib import asynccontextmanager
from typing import Dict, AsyncGenerator, Any

from fastapi import FastAPI, status, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from sqlalchemy.orm import Session
from apps.sprocket.routes import router as genai_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[Any, Any]:
    # await database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(genai_router)
add_pagination(app)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = Session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_data = {"detail": exc.errors(), "body": exc.body}
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_data)


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}
