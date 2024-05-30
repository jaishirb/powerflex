# tests/test_routes.py

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unittest
def test_create_chart_data(client: TestClient):
    response = client.post(
        "/api/v1/chart_data",
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


# @pytest.mark.asyncio
# def test_get_chart_data(initialize_tests):
#     response = client.post(
#         "/api/v1/chart_data",
#         json={
#             "SPRocket_production_actual": [10, 20, 30],
#             "SPRocket_production_goal": [15, 25, 35],
#             "time": [1, 2, 3],
#         },
#     )
#     data = response.json()
#     chart_data_id = data["id"]
#
#     response = client.get(f"/api/v1/chart_data/{chart_data_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == chart_data_id
#
#
# @pytest.mark.asyncio
# def test_create_factory():
#     response = client.post(
#         "/api/v1/factories",
#         json={
#             "chart_data": {
#                 "SPRocket_production_actual": [10, 20, 30],
#                 "SPRocket_production_goal": [15, 25, 35],
#                 "time": [1, 2, 3],
#             }
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     assert data["chart_data"]["SPRocket_production_actual"] == [10, 20, 30]
#
#
# @pytest.mark.asyncio
# def test_get_factory():
#     response = client.post(
#         "/api/v1/factories",
#         json={
#             "chart_data": {
#                 "SPRocket_production_actual": [10, 20, 30],
#                 "SPRocket_production_goal": [15, 25, 35],
#                 "time": [1, 2, 3],
#             }
#         },
#     )
#     data = response.json()
#     factory_id = data["id"]
#
#     response = client.get(f"/api/v1/factories/{factory_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == factory_id
#
#
# @pytest.mark.asyncio
# def test_create_sprocket():
#     response = client.post(
#         "/api/v1/sprockets",
#         json={
#             "teeth": 20,
#             "pitch_diameter": 5.0,
#             "outside_diameter": 6.0,
#             "pitch": 2.0,
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     assert data["teeth"] == 20
#
#
# @pytest.mark.asyncio
# def test_get_sprocket():
#     response = client.post(
#         "/api/v1/sprockets",
#         json={
#             "teeth": 20,
#             "pitch_diameter": 5.0,
#             "outside_diameter": 6.0,
#             "pitch": 2.0,
#         },
#     )
#     data = response.json()
#     sprocket_id = data["id"]
#
#     response = client.get(f"/api/v1/sprockets/{sprocket_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == sprocket_id
#
#
# @pytest.mark.asyncio
# def test_update_sprocket():
#     response = client.post(
#         "/api/v1/sprockets",
#         json={
#             "teeth": 20,
#             "pitch_diameter": 5.0,
#             "outside_diameter": 6.0,
#             "pitch": 2.0,
#         },
#     )
#     data = response.json()
#     sprocket_id = data["id"]
#
#     update_response = client.put(
#         f"/api/v1/sprockets/{sprocket_id}",
#         json={
#             "teeth": 25,
#             "pitch_diameter": 5.5,
#             "outside_diameter": 6.5,
#             "pitch": 2.5,
#         },
#     )
#     assert update_response.status_code == 200
#     update_data = update_response.json()
#     assert update_data["teeth"] == 25
#
#
# @pytest.mark.asyncio
# def test_get_sprockets():
#     client.post(
#         "/api/v1/sprockets",
#         json={
#             "teeth": 20,
#             "pitch_diameter": 5.0,
#             "outside_diameter": 6.0,
#             "pitch": 2.0,
#         },
#     )
#     client.post(
#         "/api/v1/sprockets",
#         json={
#             "teeth": 22,
#             "pitch_diameter": 5.2,
#             "outside_diameter": 6.2,
#             "pitch": 2.2,
#         },
#     )
#
#     response = client.get("/api/v1/sprockets")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 2
#     assert data[0]["teeth"] == 20
#     assert data[1]["teeth"] == 22
