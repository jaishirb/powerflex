from datetime import datetime
from typing import Annotated, Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SPRocketTypeBase(BaseModel):
    teeth: int
    pitch_diameter: float
    outside_diameter: float
    pitch: float


class SPRocketTypeCreate(SPRocketTypeBase):
    pass


class SPRocketTypeResponse(SPRocketTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SPRocketProductionBase(BaseModel):
    sprocket_production_actual: int
    sprocket_production_goal: int
    sprocket_types: List[SPRocketTypeCreate]


class SPRocketProductionCreate(SPRocketProductionBase):
    time: datetime

    @classmethod
    @field_validator("time", mode="before")
    def convert_timestamp_to_datetime(cls, value: int) -> datetime:
        return datetime.fromtimestamp(value)

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        data["time"] = int(self.time.timestamp())
        return data


class SPRocketProductionResponse(SPRocketProductionBase):
    id: int
    time: Annotated[int, Field(validate_default=True)]

    @field_validator("time", mode="before")
    @classmethod
    def convert_datetime_to_timestamp(cls, value: datetime) -> int:
        return int(value.timestamp())

    model_config = ConfigDict(from_attributes=True)


class ChartDataBase(BaseModel):
    pass


class ChartDataCreate(ChartDataBase):
    sprocket_productions: List[SPRocketProductionCreate]


class ChartDataResponse(ChartDataBase):
    id: int
    sprocket_productions: List[SPRocketProductionResponse]

    model_config = ConfigDict(from_attributes=True)


class FactoryBase(BaseModel):
    pass


class FactoryCreate(FactoryBase):
    chart_data: ChartDataCreate


class FactoryResponse(FactoryBase):
    id: int
    chart_data: ChartDataResponse

    model_config = ConfigDict(from_attributes=True)
