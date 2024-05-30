import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from apps.sprocket import schemas, services


@pytest.mark.unittest
def test_create_chart_data(client: TestClient) -> None:
    response = client.post(
        url="/api/v1/chart_data",
        json={
            "sprocket_production_actual": [10, 20, 30],
            "sprocket_production_goal": [15, 25, 35],
            "time": [1, 2, 3],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["sprocket_production_actual"] == [10, 20, 30]


@pytest.mark.unittest
def test_get_chart_data(client: TestClient, session: Session) -> None:
    chart_data = schemas.ChartDataCreate(
        sprocket_production_actual=[10, 20, 30],
        sprocket_production_goal=[15, 25, 35],
        time=[1, 2, 3],
    )
    chart_data = services.create_chart_data(session, chart_data)

    response = client.get(url=f"/api/v1/chart_data/{chart_data.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == chart_data.id


@pytest.mark.unittest
def test_create_factory(client: TestClient, session: Session) -> None:
    response = client.post(
        url="/api/v1/factories",
        json={
            "chart_data": {
                "sprocket_production_actual": [10, 20, 30],
                "sprocket_production_goal": [15, 25, 35],
                "time": [1, 2, 3],
            }
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["chart_data"]["sprocket_production_actual"] == [10, 20, 30]


@pytest.mark.unittest
def test_get_factory(client: TestClient, session: Session) -> None:
    factory_data = schemas.FactoryCreate(
        chart_data=schemas.ChartDataCreate(
            sprocket_production_actual=[10, 20, 30],
            sprocket_production_goal=[15, 25, 35],
            time=[1, 2, 3],
        )
    )
    factory = services.create_factory(session, factory_data)
    factory_id = factory.id

    response = client.get(url=f"/api/v1/factories/{factory_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == factory_id


@pytest.mark.unittest
def test_create_sprocket(client: TestClient, session: Session) -> None:
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
    sprocket_data = schemas.SPRocketCreate(
        teeth=20,
        pitch_diameter=5.0,
        outside_diameter=6.0,
        pitch=2.0,
    )
    sprocket = services.create_sprocket(session, sprocket_data)
    sprocket_id = sprocket.id

    response = client.get(url=f"/api/v1/sprockets/{sprocket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sprocket_id


@pytest.mark.unittest
def test_update_sprocket(client: TestClient, session: Session) -> None:
    sprocket_data = schemas.SPRocketCreate(
        teeth=20,
        pitch_diameter=5.0,
        outside_diameter=6.0,
        pitch=2.0,
    )
    sprocket = services.create_sprocket(session, sprocket_data)
    sprocket_id = sprocket.id

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
        sprocket_data = schemas.SPRocketCreate(
            teeth=20 * i,
            pitch_diameter=5.0 * i,
            outside_diameter=6.0 * i,
            pitch=2.0 * i,
        )
        services.create_sprocket(session, sprocket_data)

    response = client.get(url="/api/v1/sprockets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for i in range(1, 6):
        sprocket_data_response = schemas.SPRocketResponse.model_validate(
            response.json()[i - 1]
        )
        assert sprocket_data_response.teeth == 20 * i
        assert sprocket_data_response.pitch_diameter == 5.0 * i
        assert sprocket_data_response.outside_diameter == 6.0 * i
        assert sprocket_data_response.pitch == 2.0 * i
