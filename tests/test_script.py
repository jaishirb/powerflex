import json
from typing import Any
from unittest.mock import mock_open

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from apps.sprocket import models
from apps.sprocket.tasks import load_data_from_json

factory_data = {
    "factories": [
        {
            "factory": {
                "chart_data": {
                    "sprocket_production_actual": [10, 20, 30],
                    "sprocket_production_goal": [15, 25, 35],
                    "time": [1611194818, 1622194818, 1633194818],
                }
            }
        }
    ]
}

sprocket_data = {
    "sprockets": [
        {"teeth": 20, "pitch_diameter": 5.5, "outside_diameter": 6.0, "pitch": 2.5}
    ]
}


@pytest.fixture
def mock_files(mocker: Any) -> None:
    factory_json = json.dumps(factory_data)
    sprocket_json = json.dumps(sprocket_data)
    mocked_open = mock_open()
    mocked_open.side_effect = [
        mock_open(read_data=factory_json).return_value,
        mock_open(read_data=sprocket_json).return_value,
    ]
    mocker.patch("builtins.open", mocked_open)


@pytest.mark.unittest
def test_load_data_from_json(
    client: TestClient, session: Session, mock_files: Any
) -> None:
    load_data_from_json(
        factory_file_path="factory_file.json",
        sprocket_file_path="sprocket_file.json",
        session=session,
    )

    statement = select(models.ChartData)
    chart_data = session.exec(statement).all()
    assert len(chart_data) == 1

    production_actual_values = [10, 20, 30]
    production_goal_values = [15, 25, 35]
    production_time_values = [1611194818, 1622194818, 1633194818]
    for chart_data_element in chart_data:
        assert len(chart_data_element.sprocket_productions) == 3
        for index, sprocket_production in enumerate(
            chart_data_element.sprocket_productions
        ):
            assert (
                sprocket_production.sprocket_production_actual
                == production_actual_values[index]
            )
            assert (
                sprocket_production.sprocket_production_goal
                == production_goal_values[index]
            )
            assert (
                int(sprocket_production.time.timestamp())
                == production_time_values[index]
            )

    statement = select(models.Factory)
    factories = session.exec(statement).all()
    assert len(factories) == 1
    assert factories[0].chart_data_id == chart_data[0].id

    statement = select(models.SPRocketType)
    sprocket_data_objects = session.exec(statement).all()
    assert len(sprocket_data_objects) == 1

    assert sprocket_data_objects[0].teeth == 20
    assert sprocket_data_objects[0].pitch_diameter == 5.5
    assert sprocket_data_objects[0].outside_diameter == 6.0
    assert sprocket_data_objects[0].pitch == 2.5

    statement = select(models.InitialDataLoad)
    initial_data_load = session.exec(statement).all()
    assert len(initial_data_load) == 1
    assert initial_data_load[0].loaded is True
