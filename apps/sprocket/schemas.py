from typing import List

from pydantic import BaseModel, ConfigDict


class ChartDataCreate(BaseModel):
    sprocket_production_actual: List[int]
    sprocket_production_goal: List[int]
    time: List[int]


class ChartDataResponse(BaseModel):
    id: int
    sprocket_production_actual: List[int]
    sprocket_production_goal: List[int]
    time: List[int]

    model_config = ConfigDict(from_attributes=True)


class FactoryCreate(BaseModel):
    chart_data: ChartDataCreate


class FactoryResponse(BaseModel):
    id: int
    chart_data: ChartDataResponse

    model_config = ConfigDict(from_attributes=True)


class SPRocketCreate(BaseModel):
    teeth: int
    pitch_diameter: float
    outside_diameter: float
    pitch: float


class SPRocketResponse(BaseModel):
    id: int
    teeth: int
    pitch_diameter: float
    outside_diameter: float
    pitch: float

    model_config = ConfigDict(from_attributes=True)


class SPRocketUpdate(BaseModel):
    teeth: int
    pitch_diameter: float
    outside_diameter: float
    pitch: float
