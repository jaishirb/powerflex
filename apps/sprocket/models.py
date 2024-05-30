from typing import List, Optional

from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import SQLModel, Field, Relationship, Column

metadata = SQLModel.metadata


class ChartData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sprocket_production_actual: List[int] = Field(sa_column=Column(JSON))
    sprocket_production_goal: List[int] = Field(sa_column=Column(JSON))
    time: List[int] = Field(sa_column=Column(JSON))
    factories: List["Factory"] = Relationship(back_populates="chart_data")

    def __str__(self) -> str:
        return f"{self.id}"


class Factory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chart_data_id: Optional[int] = Field(default=None, foreign_key="chartdata.id")
    chart_data: Optional[ChartData] = Relationship(back_populates="factories")


class SPRocket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teeth: int
    pitch_diameter: float
    outside_diameter: float
    pitch: float

    def __str__(self) -> str:
        return f"{self.id}"


class InitialDataLoad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loaded: bool = False

    def __str__(self) -> str:
        return f"{self.id}"
