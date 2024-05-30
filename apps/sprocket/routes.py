from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from apps.sprocket import dependencies
from apps.sprocket import schemas
from apps.sprocket import services
from apps.database import database

router = APIRouter(prefix="/api/v1", tags=["v1"])


# ChartData CRUD
@router.post(path="/chart_data", response_model=schemas.ChartDataResponse)
def create_chart_data(
    chart_data: schemas.ChartDataCreate,
    session: database.SessionDep,
):
    return services.create_chart_data(session, chart_data)


# @router.get(
#     path="/chart_data/{chart_data_id}", response_model=schemas.ChartDataResponse
# )
# async def get_chart_data(
#     chart_data_id: int, session: AsyncSession = Depends(dependencies.get_session)
# ):
#     chart_data = await services.get_chart_data(session, chart_data_id)
#     if not chart_data:
#         raise HTTPException(status_code=404, detail="ChartData not found")
#     return chart_data
#
#
# # Factory CRUD
# @router.post(path="/factories", response_model=schemas.FactoryResponse)
# async def create_factory(
#     factory: schemas.FactoryCreate,
#     session: AsyncSession = Depends(dependencies.get_session),
# ):
#     return await services.create_factory(session, factory)
#
#
# @router.get(path="/factories/{factory_id}", response_model=schemas.FactoryResponse)
# async def get_factory(
#     factory_id: int, session: AsyncSession = Depends(dependencies.get_session)
# ):
#     factory = await services.get_factory(session, factory_id)
#     if not factory:
#         raise HTTPException(status_code=404, detail="Factory not found")
#     return factory
#
#
# # SPRocket CRUD
# @router.get(path="/sprockets", response_model=List[schemas.SPRocketResponse])
# async def get_sprockets(session: AsyncSession = Depends(dependencies.get_session)):
#     return await services.get_sprockets(session)
#
#
# @router.post(path="/sprockets", response_model=schemas.SPRocketResponse)
# async def create_sprocket(
#     sprocket: schemas.SPRocketCreate,
#     session: AsyncSession = Depends(dependencies.get_session),
# ):
#     return await services.create_sprocket(session, sprocket)
#
#
# @router.put(path="/sprockets/{sprocket_id}", response_model=schemas.SPRocketResponse)
# async def update_sprocket(
#     sprocket_id: int,
#     sprocket: schemas.SPRocketUpdate,
#     session: AsyncSession = Depends(dependencies.get_session),
# ):
#     sprocket = await services.update_sprocket(session, sprocket_id, sprocket)
#     if not sprocket:
#         raise HTTPException(status_code=404, detail="Sprocket not found")
#     return sprocket
