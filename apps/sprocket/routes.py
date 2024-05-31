from typing import List, Type

from fastapi import APIRouter, HTTPException
from sqlalchemy import ScalarResult

from apps.database import database
from apps.sprocket import models, schemas, services

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
) -> Type[models.ChartData]:
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


# SPRocketType CRUD
@router.get(path="/sprockets", response_model=List[schemas.SPRocketTypeResponse])
def get_sprockets_types(
    session: database.SessionDep,
) -> ScalarResult[models.SPRocketType]:
    return services.get_sprocket_types(session)


@router.get(
    path="/sprockets/{sprocket_id}", response_model=schemas.SPRocketTypeResponse
)
def get_sprocket(sprocket_id: int, session: database.SessionDep) -> models.SPRocketType:
    sprocket = services.get_sprocket_type(session, sprocket_id)
    if not sprocket:
        raise HTTPException(status_code=404, detail="Sprocket not found")
    return sprocket


@router.post(path="/sprockets", response_model=schemas.SPRocketTypeResponse)
def create_sprocket(
    sprocket: schemas.SPRocketTypeCreate,
    session: database.SessionDep,
) -> models.SPRocketType:
    return services.create_sprocket_type(session, sprocket)


@router.put(
    path="/sprockets/{sprocket_id}", response_model=schemas.SPRocketTypeResponse
)
def update_sprocket(
    sprocket_id: int,
    sprocket: schemas.SPRocketTypeCreate,
    session: database.SessionDep,
) -> Type[models.SPRocketType]:
    updated_sprocket = services.update_sprocket_type(session, sprocket_id, sprocket)
    if not updated_sprocket:
        raise HTTPException(status_code=404, detail="Sprocket not found")
    return updated_sprocket


@router.post(
    path="/sprocket_production/", response_model=schemas.SPRocketProductionResponse
)
def create_sprocket_production(
    sprocket_production: schemas.SPRocketProductionCreate,
    session: database.SessionDep,
) -> models.SPRocketProduction:
    return services.create_sprocket_production(session, sprocket_production)


@router.get(
    path="/sprocket_production/{sprocket_production_id}",
    response_model=schemas.SPRocketProductionResponse,
)
def read_sprocket_production(
    sprocket_production_id: int,
    session: database.SessionDep,
) -> Type[models.SPRocketProduction]:
    sprocket_production = services.get_sprocket_production(
        session, sprocket_production_id
    )
    if sprocket_production is None:
        raise HTTPException(status_code=404, detail="Sprocket production not found")
    return sprocket_production


@router.get(
    path="/sprocket_production/",
    response_model=List[schemas.SPRocketProductionResponse],
)
def read_all_sprocket_production(
    session: database.SessionDep,
) -> ScalarResult[models.SPRocketProduction]:
    return services.get_all_sprocket_production(session)
