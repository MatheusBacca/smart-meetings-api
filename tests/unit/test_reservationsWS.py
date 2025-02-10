from datetime import datetime, timedelta
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
    mock_query = mock_db.query.return_value
    mock_query.count.return_value = len(mock_reservations)
    mock_query.offset.return_value.limit.return_value.all.return_value = (
        mock_reservations
    )

    response = client.get("/reservations")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "page": 1,
        "limit": 10,
        "total_items": 2,
        "total_pages": 1,
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
        ],
    }


def test_list_reservations_with_pagination(mock_db: MagicMock):
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
        Reservations(
            id=3,
            room_id=103,
            user_id=3,
            start_time=datetime(2025, 2, 12, 14, 0),
            end_time=datetime(2025, 2, 12, 16, 0),
        ),
    ]
    mock_query = mock_db.query.return_value
    mock_query.count.return_value = len(mock_reservations)
    mock_query.offset.return_value.limit.return_value.all.return_value = (
        mock_reservations[:2]
    )

    response = client.get("/reservations", params={"page": 1, "limit": 2})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "page": 1,
        "limit": 2,
        "total_items": 3,
        "total_pages": 2,
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
        ],
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
    mock_query = mock_db.query.return_value
    mock_query.filter.return_value.count.return_value = len(mock_reservations)
    mock_query.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_reservations

    response = client.get("/reservations", params={"date": "2025-02-10"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "page": 1,
        "limit": 10,
        "total_items": 1,
        "total_pages": 1,
        "reservations": [
            {
                "id": 1,
                "room_id": 101,
                "user_id": 1,
                "start_time": "2025-02-10T10:00:00",
                "end_time": "2025-02-10T12:00:00",
            },
        ],
    }


def test_create_reservation_start_time_in_past(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = Users(
        id=1, name="Test User", email="user@test.com"
    )

    reservation_request = {
        "room_id": 101,
        "user_name": "Test User",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(),
    }

    response = client.post("/reservations/", json=reservation_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "The start time cannot be in the past."


def test_create_reservation_conflict(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = Users(
        id=1, name="Test User", email="user@test.com"
    )

    start_time = datetime.now() + timedelta(hours=1)
    end_time = datetime.now() + timedelta(hours=1, minutes=30)

    mock_db.query.return_value.filter.return_value.first.return_value = Reservations(
        id=1,
        room_id=101,
        user_id=1,
        start_time=start_time,
        end_time=end_time,
    )

    reservation_request = {
        "room_id": 101,
        "user_name": "Test User",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
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
