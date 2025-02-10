from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import status
from database.database import get_db
from util.utils import create_app
from database.models import Reservations, Users

app = create_app()
client = TestClient(app)


@pytest.fixture
def mock_db():
    mock = MagicMock()
    mock.query.return_value.filter.return_value.first.return_value = None
    return mock


@pytest.fixture(autouse=True)
def override_dependency(mock_db: MagicMock):
    app.dependency_overrides[get_db] = lambda: mock_db
    global client
    client = TestClient(app)


def test_list_reservations_no_filters(mock_db: MagicMock):
    mock_reservations = [
        Reservations(
            id=1,
            room_id=101,
            user_id=1,
            start_time=datetime(2025, 2, 10, 10, 0),
            end_time=datetime(2025, 2, 10, 12, 0),
        ),
        Reservations(
            id=2,
            room_id=102,
            user_id=2,
            start_time=datetime(2025, 2, 11, 9, 0),
            end_time=datetime(2025, 2, 11, 11, 0),
        ),
    ]
    mock_db.query.return_value.all.return_value = mock_reservations

    response = client.get("/reservations/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "reservations": [
            {
                "id": 1,
                "room_id": 101,
                "user_id": 1,
                "start_time": "2025-02-10T10:00:00",
                "end_time": "2025-02-10T12:00:00",
            },
            {
                "id": 2,
                "room_id": 102,
                "user_id": 2,
                "start_time": "2025-02-11T09:00:00",
                "end_time": "2025-02-11T11:00:00",
            },
        ]
    }


def test_list_reservations_with_date_filter(mock_db: MagicMock):
    mock_reservations = [
        Reservations(
            id=1,
            room_id=101,
            user_id=1,
            start_time=datetime(2025, 2, 10, 10, 0),
            end_time=datetime(2025, 2, 10, 12, 0),
        ),
    ]
    mock_db.query.return_value.filter.return_value.all.return_value = mock_reservations

    response = client.get("/reservations/", params={"date": "2025-02-10"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "reservations": [
            {
                "id": 1,
                "room_id": 101,
                "user_id": 1,
                "start_time": "2025-02-10T10:00:00",
                "end_time": "2025-02-10T12:00:00",
            },
        ]
    }


def test_create_reservation_start_time_in_past(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = (
        None  # Nenhuma reserva existente
    )
    mock_db.query.return_value.filter.return_value.first.return_value = Users(
        id=1, name="Test User", email="user@test.com"
    )  # Usuário encontrado

    reservation_request = {
        "room_id": 101,
        "user_name": "Test User",
        "start_time": "2023-02-10T10:00:00",  # Hora no passado
        "end_time": "2023-02-10T12:00:00",
    }

    response = client.post("/reservations/", json=reservation_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "The start time cannot be in the past."


def test_create_reservation_conflict(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = Users(
        id=1, name="Test User", email="user@test.com"
    )

    mock_db.query.return_value.filter.return_value.first.return_value = Reservations(
        id=1,
        room_id=101,
        user_id=1,
        start_time=datetime(2025, 2, 10, 9, 0),
        end_time=datetime(2025, 2, 10, 11, 0),
    )

    reservation_request = {
        "room_id": 101,
        "user_name": "Test User",
        "start_time": "2025-02-10T10:00:00",
        "end_time": "2025-02-10T12:00:00",
    }

    response = client.post("/reservations", json=reservation_request)

    response_data = response.json()
    assert "detail" in response_data
    assert "message" in response_data["detail"]
    assert (
        response_data["detail"]["message"]
        == "The requested reservation conflicts with an existing reservation."
    )

    assert "conflicting_reservation" in response_data["detail"]
    conflicting_reservation = response_data["detail"]["conflicting_reservation"]
    assert "id" in conflicting_reservation
    assert "room_id" in conflicting_reservation
    assert "start_time" in conflicting_reservation
    assert "end_time" in conflicting_reservation


def test_delete_reservation_success(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = Reservations(
        id=1,
        room_id=101,
        user_id=1,
        start_time=datetime(2025, 2, 10, 10, 0),
        end_time=datetime(2025, 2, 10, 12, 0),
    )

    response = client.delete("/reservations/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT
