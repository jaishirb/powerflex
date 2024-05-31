from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

metadata = SQLModel.metadata


class SPRocketType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teeth: int
    pitch_diameter: float
    outside_diameter: float
    pitch: float
    production_id: Optional[int] = Field(
        default=None, foreign_key="sprocketproduction.id"
    )
    production: Optional["SPRocketProduction"] = Relationship(
        back_populates="sprocket_types"
    )

    def __str__(self) -> str:
        return f"{self.id}"


class SPRocketProduction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sprocket_production_actual: int
    sprocket_production_goal: int
    time: datetime
    sprocket_types: List[SPRocketType] = Relationship(back_populates="production")
    chart_data_id: Optional[int] = Field(default=None, foreign_key="chartdata.id")
    chart_data: Optional["ChartData"] = Relationship(
        back_populates="sprocket_productions"
    )

    def __str__(self) -> str:
        return f"{self.id}"


class ChartData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sprocket_productions: List[SPRocketProduction] = Relationship(
        back_populates="chart_data"
    )
    factory: Optional["Factory"] = Relationship(
        back_populates="chart_data",
    )

    def __str__(self) -> str:
        return f"{self.id}"


class Factory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chart_data_id: Optional[int] = Field(default=None, foreign_key="chartdata.id")
    chart_data: Optional[ChartData] = Relationship(back_populates="factory")

    def __str__(self) -> str:
        return f"{self.id}"


class InitialDataLoad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loaded: bool = False

    def __str__(self) -> str:
        return f"{self.id}"
