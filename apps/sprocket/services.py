from typing import Optional, Type

from fastapi import HTTPException
from sqlalchemy import ScalarResult
from sqlmodel import Session, select

from apps.sprocket import models, schemas
from apps.sprocket.models import SPRocket


def create_chart_data(
    session: Session, chart_data: schemas.ChartDataCreate
) -> models.ChartData:
    session_chart_data = models.ChartData.model_validate(chart_data)
    session.add(session_chart_data)
    session.commit()
    session.refresh(session_chart_data)
    return session_chart_data


def get_chart_data(session: Session, chart_data_id: int) -> models.ChartData:
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


def get_sprocket(session: Session, sprocket_id: int) -> Optional[models.SPRocket]:
    result = session.get(models.SPRocket, sprocket_id)
    return result


def get_sprockets(
    session: Session, page: int = 1, limit: int = 10
) -> ScalarResult[SPRocket]:
    offset = (page - 1) * limit
    stmt = select(models.SPRocket).limit(limit).offset(offset)
    result = session.exec(stmt)
    return result


def create_sprocket(
    session: Session, sprocket: schemas.SPRocketCreate
) -> models.SPRocket:
    session_sprocket = models.SPRocket.model_validate(sprocket)
    session.add(session_sprocket)
    session.commit()
    session.refresh(session_sprocket)
    return session_sprocket


def update_sprocket(
    session: Session, sprocket_id: int, sprocket: schemas.SPRocketUpdate
) -> Type[SPRocket]:
    result = session.get(models.SPRocket, sprocket_id)
    if not result:
        raise HTTPException(status_code=404, detail="sprocket not found")
    update_dict = sprocket.model_dump(exclude_unset=True)
    result.sqlmodel_update(obj=update_dict)
    session.add(result)
    session.commit()
    session.refresh(result)
    return result
