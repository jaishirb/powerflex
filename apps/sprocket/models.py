from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import event
from sqlmodel import Field, Relationship, SQLModel

metadata = SQLModel.metadata


class BaseSQLModel(SQLModel):
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        event.listen(cls, "before_update", cls.set_updated_at)

    @staticmethod
    def set_updated_at(mapper: Any, connection: Any, target: Any) -> None:
        target.updated_at = datetime.now()


class SPRocketType(BaseSQLModel, table=True):
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


class SPRocketProduction(BaseSQLModel, table=True):
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


class ChartData(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sprocket_productions: List[SPRocketProduction] = Relationship(
        back_populates="chart_data"
    )
    factory: Optional["Factory"] = Relationship(
        back_populates="chart_data",
    )

    def __str__(self) -> str:
        return f"{self.id}"


class Factory(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chart_data_id: Optional[int] = Field(default=None, foreign_key="chartdata.id")
    chart_data: Optional[ChartData] = Relationship(back_populates="factory")

    def __str__(self) -> str:
        return f"{self.id}"


class InitialDataLoad(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loaded: bool = False

    def __str__(self) -> str:
        return f"{self.id}"
