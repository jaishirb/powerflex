import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict

from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_redis_cache import FastApiRedisCache
from sqlalchemy.orm import Session

from apps.sprocket.routes import router as sprocket_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[Any, Any]:
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL"),
        prefix="powerflex-cache",
        response_header="X-PowerFlex-Cache",
        ignore_arg_types=[Request, Response, Session],
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    title="POWERFLEX API",
    description="This is an API for POWERFLEX Technical Test",
    summary="Build a RESTful api that services requests for sprocket factory data and sprockets.",
    version="1.0",
    terms_of_service="https://www.powerflex.com/terms-and-conditions",
    contact={
        "name": "Jaishir Bayuelo",
        "url": "https://www.linkedin.com/in/jaisir-bayuelo-85a0b6160/",
        "email": "jaisirenterprise@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "Apache 2.0",
    },
)

app.include_router(router=sprocket_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next: Any) -> Response:
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
