from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from apps.sprocket import schemas, services


def create_sprocket_type(
    session: Session,
    teeth: int,
    pitch_diameter: float,
    outside_diameter: float,
    pitch: float,
):
    return services.create_sprocket_type(
        session=session,
        sprocket_type=schemas.SPRocketTypeCreate(
            teeth=teeth,
            pitch_diameter=pitch_diameter,
            outside_diameter=outside_diameter,
            pitch=pitch,
        ),
    ).id


def create_chart_data(session: Session, sprocket_productions=[]):
    return services.create_chart_data(
        session=session,
        chart_data=schemas.ChartDataCreate(sprocket_productions=sprocket_productions),
    )


def create_sprocket_production(
    session: Session,
    actual: int,
    goal: int,
    time: datetime,
    sprocket_types: list,
    chart_data_id: int,
):
    sprocket_production_data = schemas.SPRocketProductionCreate(
        sprocket_production_actual=actual,
        sprocket_production_goal=goal,
        time=time,
        sprocket_types=sprocket_types,
        chart_data_id=chart_data_id,
    )
    return services.create_sprocket_production(
        session=session, sprocket_production=sprocket_production_data
    )


def assert_sprocket_production_response(
    session: Session,
    data: dict,
    actual: int,
    goal: int,
    time: datetime,
    sprocket_types: list,
):
    assert data["sprocket_production_actual"] == actual
    assert data["sprocket_production_goal"] == goal
    assert data["time"] == int(time.timestamp())
    assert len(data["sprocket_types"]) == len(sprocket_types)

    for i, sprocket_type in enumerate(sprocket_types):
        sprocket_type_obj = services.get_sprocket_type(
            session=session, sprocket_type_id=sprocket_type
        )
        assert data["sprocket_types"][i]["teeth"] == sprocket_type_obj.teeth
        assert (
            data["sprocket_types"][i]["pitch_diameter"]
            == sprocket_type_obj.pitch_diameter
        )
        assert (
            data["sprocket_types"][i]["outside_diameter"]
            == sprocket_type_obj.outside_diameter
        )
        assert data["sprocket_types"][i]["pitch"] == sprocket_type_obj.pitch


@pytest.mark.unittest
def test_create_chart_data(client: TestClient, session: Session) -> None:
    sprocket_types = [
        create_sprocket_type(
            session=session,
            teeth=5,
            pitch_diameter=5.0,
            outside_diameter=6.0,
            pitch=1.0,
        )
    ]
    time = datetime(2024, 5, 30, 12, 0, 0)
    chart_data = create_chart_data(session=session)
    sprocket_production = create_sprocket_production(
        session=session,
        actual=10,
        goal=20,
        time=time,
        sprocket_types=sprocket_types,
        chart_data_id=chart_data.id,
    )

    response = client.post(
        url="/api/v1/chart_data",
        json={"sprocket_productions": [sprocket_production.id]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert_sprocket_production_response(
        session=session,
        data=data["sprocket_productions"][0],
        actual=10,
        goal=20,
        time=time,
        sprocket_types=sprocket_types,
    )


@pytest.mark.unittest
def test_get_chart_data(client: TestClient, session: Session) -> None:
    sprocket_type = create_sprocket_type(
        session=session, teeth=20, pitch_diameter=5.5, outside_diameter=6.0, pitch=2.5
    )
    chart_data = create_chart_data(session=session)
    sprocket_production = create_sprocket_production(
        session=session,
        actual=10,
        goal=15,
        time=datetime(2024, 5, 30, 12, 0, 0),
        sprocket_types=[sprocket_type],
        chart_data_id=chart_data.id,
    )
    chart_data = create_chart_data(
        session=session, sprocket_productions=[sprocket_production.id]
    )

    response = client.get(url=f"/api/v1/chart_data/{chart_data.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == chart_data.id


@pytest.mark.unittest
def test_create_factory(client: TestClient, session: Session) -> None:
    sprocket_types = [
        create_sprocket_type(
            session=session,
            teeth=5,
            pitch_diameter=5.0,
            outside_diameter=6.0,
            pitch=1.0,
        )
    ]
    time = datetime(2024, 5, 30, 12, 0, 0)
    chart_data = create_chart_data(session=session)
    sprocket_production = create_sprocket_production(
        session=session,
        actual=10,
        goal=20,
        time=time,
        sprocket_types=sprocket_types,
        chart_data_id=chart_data.id,
    )
    chart_data = create_chart_data(
        session=session, sprocket_productions=[sprocket_production.id]
    )

    response = client.post(
        url="/api/v1/factories",
        json={"chart_data": chart_data.id},
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert (
        data["chart_data"]["sprocket_productions"][0]["sprocket_production_actual"]
        == 10
    )
    assert (
        data["chart_data"]["sprocket_productions"][0]["sprocket_production_goal"] == 20
    )


@pytest.mark.unittest
def test_get_factory(client: TestClient, session: Session) -> None:
    sprocket_types = [
        create_sprocket_type(
            session=session,
            teeth=20,
            pitch_diameter=5.5,
            outside_diameter=6.0,
            pitch=2.5,
        )
    ]
    chart_data = create_chart_data(session=session)
    sprocket_production = create_sprocket_production(
        session=session,
        actual=10,
        goal=15,
        time=datetime(2024, 5, 30, 12, 0, 0),
        sprocket_types=sprocket_types,
        chart_data_id=chart_data.id,
    )
    chart_data_obj = create_chart_data(
        session=session, sprocket_productions=[sprocket_production.id]
    )
    factory_data = schemas.FactoryCreate(chart_data=chart_data_obj.id)
    created_factory = services.create_factory(session=session, factory=factory_data)
    factory_id = created_factory.id

    response = client.get(url=f"/api/v1/factories/{factory_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == factory_id


@pytest.mark.unittest
def test_create_sprocket(client: TestClient) -> None:
    response = client.post(
        url="/api/v1/sprockets",
        json={
            "teeth": 20,
            "pitch_diameter": 5.0,
            "outside_diameter": 6.0,
            "pitch": 2.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["teeth"] == 20


@pytest.mark.unittest
def test_get_sprocket(client: TestClient, session: Session) -> None:
    sprocket_data = schemas.SPRocketTypeCreate(
        teeth=20,
        pitch_diameter=5.0,
        outside_diameter=6.0,
        pitch=2.0,
    )
    created_sprocket = services.create_sprocket_type(
        session=session, sprocket_type=sprocket_data
    )
    sprocket_id = created_sprocket.id

    response = client.get(url=f"/api/v1/sprockets/{sprocket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sprocket_id


@pytest.mark.unittest
def test_update_sprocket(client: TestClient, session: Session) -> None:
    sprocket_data = schemas.SPRocketTypeCreate(
        teeth=20,
        pitch_diameter=5.0,
        outside_diameter=6.0,
        pitch=2.0,
    )
    created_sprocket = services.create_sprocket_type(
        session=session, sprocket_type=sprocket_data
    )
    sprocket_id = created_sprocket.id

    update_response = client.put(
        url=f"/api/v1/sprockets/{sprocket_id}",
        json={
            "teeth": 25,
            "pitch_diameter": 5.5,
            "outside_diameter": 6.5,
            "pitch": 2.5,
        },
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["teeth"] == 25


@pytest.mark.unittest
def test_get_sprockets(client: TestClient, session: Session) -> None:
    for i in range(1, 6):
        sprocket_data = schemas.SPRocketTypeCreate(
            teeth=20 * i,
            pitch_diameter=5.0 * i,
            outside_diameter=6.0 * i,
            pitch=2.0 * i,
        )
        services.create_sprocket_type(session=session, sprocket_type=sprocket_data)

    response = client.get(url="/api/v1/sprockets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for i in range(1, 6):
        sprocket_data_response = schemas.SPRocketTypeResponse.model_validate(
            data[i - 1]
        )
        assert sprocket_data_response.teeth == 20 * i
        assert sprocket_data_response.pitch_diameter == 5.0 * i
        assert sprocket_data_response.outside_diameter == 6.0 * i
        assert sprocket_data_response.pitch == 2.0 * i


@pytest.mark.unittest
def test_create_sprocket_production(client: TestClient, session: Session) -> None:
    sprocket_types_data = [
        create_sprocket_type(
            session=session,
            teeth=5 * i,
            pitch_diameter=5.0 * i,
            outside_diameter=6.0 * i,
            pitch=1.0 * i,
        )
        for i in range(1, 4)
    ]
    chart_data = create_chart_data(session=session)
    timestamp = 1633194818
    sprocket_production_data = schemas.SPRocketProductionCreate(
        sprocket_production_actual=10,
        sprocket_production_goal=15,
        time=timestamp,
        sprocket_types=sprocket_types_data,
        chart_data_id=chart_data.id,
    )
    response = client.post(
        url="/api/v1/sprocket_production",
        json=sprocket_production_data.model_dump(),
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["sprocket_production_actual"] == 10
    assert data["sprocket_production_goal"] == 15
    assert data["time"] == timestamp
    assert len(data["sprocket_types"]) == len(sprocket_types_data)
    for i, sprocket_type in enumerate(sprocket_types_data):
        sprocket_type_obj = services.get_sprocket_type(
            session=session, sprocket_type_id=sprocket_type
        )
        assert data["sprocket_types"][i]["teeth"] == sprocket_type_obj.teeth
        assert (
            data["sprocket_types"][i]["pitch_diameter"]
            == sprocket_type_obj.pitch_diameter
        )
        assert (
            data["sprocket_types"][i]["outside_diameter"]
            == sprocket_type_obj.outside_diameter
        )
        assert data["sprocket_types"][i]["pitch"] == sprocket_type_obj.pitch


@pytest.mark.unittest
def test_get_sprocket_production(client: TestClient, session: Session) -> None:
    sprocket_types = [
        create_sprocket_type(
            session=session,
            teeth=20,
            pitch_diameter=5.5,
            outside_diameter=6.0,
            pitch=2.5,
        )
    ]
    chart_data = create_chart_data(session=session)
    sprocket_production = create_sprocket_production(
        session=session,
        actual=10,
        goal=15,
        time=datetime(2024, 5, 30, 12, 0, 0),
        sprocket_types=sprocket_types,
        chart_data_id=chart_data.id,
    )

    response = client.get(url=f"/api/v1/sprocket_production/{sprocket_production.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sprocket_production.id


@pytest.mark.unittest
def test_get_all_sprocket_production(client: TestClient, session: Session) -> None:
    sprocket_types = [
        create_sprocket_type(
            session=session,
            teeth=20,
            pitch_diameter=5.5,
            outside_diameter=6.0,
            pitch=2.5,
        )
    ]
    chart_data = create_chart_data(session=session)
    sprocket_production_data_list = [
        create_sprocket_production(
            session=session,
            actual=10 * i,
            goal=15 * i,
            time=datetime(2024, 5, 30, 12, 0, 0),
            sprocket_types=sprocket_types,
            chart_data_id=chart_data.id,
        )
        for i in range(1, 4)
    ]

    response = client.get(url="/api/v1/sprocket_production")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == len(sprocket_production_data_list)
    for i, sprocket_production_data in enumerate(sprocket_production_data_list):
        assert (
            data[i]["sprocket_production_actual"]
            == sprocket_production_data.sprocket_production_actual
        )
        assert (
            data[i]["sprocket_production_goal"]
            == sprocket_production_data.sprocket_production_goal
        )
        assert data[i]["time"] == sprocket_production_data.time.timestamp()
        assert len(data[i]["sprocket_types"]) == 1

        sprocket_type_obj = services.get_sprocket_type(
            session=session, sprocket_type_id=data[i]["sprocket_types"][0]["id"]
        )
        assert data[i]["sprocket_types"][0]["teeth"] == sprocket_type_obj.teeth
        assert (
            data[i]["sprocket_types"][0]["pitch_diameter"]
            == sprocket_type_obj.pitch_diameter
        )
        assert (
            data[i]["sprocket_types"][0]["outside_diameter"]
            == sprocket_type_obj.outside_diameter
        )
        assert data[i]["sprocket_types"][0]["pitch"] == sprocket_type_obj.pitch
