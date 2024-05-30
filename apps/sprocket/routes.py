from typing import List, Type

from fastapi import APIRouter, HTTPException
from sqlalchemy import ScalarResult

from apps.database import database
from apps.sprocket import models, schemas, services
from apps.sprocket.models import SPRocket

router = APIRouter(prefix="/api/v1")


# ChartData CRUD
@router.post(path="/chart_data", response_model=schemas.ChartDataResponse)
def create_chart_data(
    chart_data: schemas.ChartDataCreate,
    session: database.SessionDep,
) -> models.ChartData:
    return services.create_chart_data(session, chart_data)


@router.get(
    path="/chart_data/{chart_data_id}", response_model=schemas.ChartDataResponse
)
def get_chart_data(
    chart_data_id: int,
    session: database.SessionDep,
) -> models.ChartData:
    chart_data = services.get_chart_data(session, chart_data_id)
    if not chart_data:
        raise HTTPException(status_code=404, detail="ChartData not found")
    return chart_data


# Factory CRUD
@router.post(path="/factories", response_model=schemas.FactoryResponse)
def create_factory(
    factory: schemas.FactoryCreate,
    session: database.SessionDep,
) -> models.Factory:
    return services.create_factory(session, factory)


@router.get(path="/factories/{factory_id}", response_model=schemas.FactoryResponse)
def get_factory(factory_id: int, session: database.SessionDep) -> models.Factory:
    factory = services.get_factory(session, factory_id)
    if not factory:
        raise HTTPException(status_code=404, detail="Factory not found")
    return factory


# SPRocket CRUD
@router.get(path="/sprockets", response_model=List[schemas.SPRocketResponse])
def get_sprockets(session: database.SessionDep) -> ScalarResult[SPRocket]:
    return services.get_sprockets(session)


@router.get(path="/sprockets/{sprocket_id}", response_model=schemas.SPRocketResponse)
def get_sprocket(sprocket_id: int, session: database.SessionDep) -> models.SPRocket:
    sprocket = services.get_sprocket(session, sprocket_id)
    if not sprocket_id:
        raise HTTPException(status_code=404, detail="sprocket not found")
    return sprocket


@router.post(path="/sprockets", response_model=schemas.SPRocketResponse)
def create_sprocket(
    sprocket: schemas.SPRocketCreate,
    session: database.SessionDep,
) -> models.SPRocket:
    return services.create_sprocket(session, sprocket)


@router.put(path="/sprockets/{sprocket_id}", response_model=schemas.SPRocketResponse)
def update_sprocket(
    sprocket_id: int,
    sprocket: schemas.SPRocketUpdate,
    session: database.SessionDep,
) -> Type[SPRocket]:
    sprocket = services.update_sprocket(session, sprocket_id, sprocket)
    if not sprocket:
        raise HTTPException(status_code=404, detail="Sprocket not found")
    return sprocket
