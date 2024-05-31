from typing import Optional, Type

from fastapi import HTTPException
from sqlalchemy import ScalarResult
from sqlmodel import Session, select

from apps.sprocket import models, schemas
from apps.sprocket.models import ChartData


def create_sprocket_type(
    session: Session, sprocket_type: schemas.SPRocketTypeCreate
) -> models.SPRocketType:
    session_sprocket_type = models.SPRocketType(**sprocket_type.model_dump())
    session.add(session_sprocket_type)
    session.commit()
    session.refresh(session_sprocket_type)
    return session_sprocket_type


def create_sprocket_production(
    session: Session, sprocket_production: schemas.SPRocketProductionCreate
) -> models.SPRocketProduction:
    sprocket_types = [
        create_sprocket_type(session, st) for st in sprocket_production.sprocket_types
    ]
    session_sprocket_production = models.SPRocketProduction(
        sprocket_production_actual=sprocket_production.sprocket_production_actual,
        sprocket_production_goal=sprocket_production.sprocket_production_goal,
        time=sprocket_production.time,
        sprocket_types=sprocket_types,
    )
    session.add(session_sprocket_production)
    session.commit()
    session.refresh(session_sprocket_production)
    return session_sprocket_production


def get_sprocket_production(
    session: Session, sprocket_production_id: int
) -> Type[models.SPRocketProduction]:
    return session.get(models.SPRocketProduction, sprocket_production_id)


def get_all_sprocket_production(
    session: Session, page: int = 1, limit: int = 10
) -> ScalarResult[models.SPRocketProduction]:
    offset = (page - 1) * limit
    stmt = select(models.SPRocketProduction).limit(limit).offset(offset)
    result = session.exec(stmt)
    return result


def create_chart_data(
    session: Session, chart_data: schemas.ChartDataCreate
) -> models.ChartData:
    sprocket_productions = [
        create_sprocket_production(session, sp)
        for sp in chart_data.sprocket_productions
    ]
    session_chart_data = models.ChartData(sprocket_productions=sprocket_productions)
    session.add(session_chart_data)
    session.commit()
    session.refresh(session_chart_data)
    return session_chart_data


def get_chart_data(session: Session, chart_data_id: int) -> Type[ChartData]:
    result = session.get(models.ChartData, chart_data_id)
    if not result:
        raise HTTPException(status_code=404, detail="Chart data not found")
    return result


def create_factory(session: Session, factory: schemas.FactoryCreate) -> models.Factory:
    chart_data = create_chart_data(session, factory.chart_data)
    session_factory = models.Factory(chart_data_id=chart_data.id)
    session.add(session_factory)
    session.commit()
    session.refresh(session_factory)
    return session_factory


def get_factory(session: Session, factory_id: int) -> Optional[models.Factory]:
    result = session.get(models.Factory, factory_id)
    return result


def get_sprocket_type(
    session: Session, sprocket_type_id: int
) -> Optional[models.SPRocketType]:
    result = session.get(models.SPRocketType, sprocket_type_id)
    return result


def get_sprocket_types(
    session: Session, page: int = 1, limit: int = 10
) -> ScalarResult[models.SPRocketType]:
    offset = (page - 1) * limit
    stmt = select(models.SPRocketType).limit(limit).offset(offset)
    result = session.exec(stmt)
    return result


def update_sprocket_type(
    session: Session, sprocket_type_id: int, sprocket_type: schemas.SPRocketTypeCreate
) -> Type[models.SPRocketType]:
    result = session.get(models.SPRocketType, sprocket_type_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sprocket type not found")
    update_dict = sprocket_type.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(result, key, value)
    session.add(result)
    session.commit()
    session.refresh(result)
    return result
