from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, date

import pytest
from database.database import get_db
from database.models import Rooms, Reservations
from util.utils import create_app

app = create_app()
client = TestClient(app)


@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    return mock_db


@pytest.fixture(autouse=True)
def override_dependency(mock_db: MagicMock):
    app.dependency_overrides[get_db] = lambda: mock_db
    global client
    client = TestClient(app)


def test_list_rooms(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.count.return_value = 1
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.count.return_value = 1

    def test_create_room(mock_db: MagicMock):
        room_data = {
            "name": "Room A",
            "location": "1st Floor",
            "capacity": 10,
            "creator_id": 1,
        }

        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = Rooms(
            id=1,
            name="Room A",
            location="1st Floor",
            capacity=10,
            creator_id=1,
            created_at=date.today(),
        )

        response = client.post("/rooms", json=room_data)

        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Room A",
            "location": "1st Floor",
            "capacity": 10,
            "creator_id": 1,
            "created_at": str(date.today()),
        }


def test_get_room_details(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = Rooms(
        id=1,
        name="Room A",
        location="1st Floor",
        capacity=10,
        creator_id=1,
        created_at=date.today(),
    )
    mock_db.query.return_value.filter.return_value.count.return_value = 1
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
        Rooms(
            id=1,
            name="Room A",
            location="1st Floor",
            capacity=10,
            creator_id=1,
            created_at=date.today(),
        )
    ]

    response = client.get("/rooms?id=1")

    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "limit": 10,
        "total_items": 1,
        "total_pages": 1,
        "rooms": [
            {
                "id": 1,
                "name": "Room A",
                "location": "1st Floor",
                "capacity": 10,
                "creator_id": 1,
                "created_at": str(date.today()),
            }
        ],
    }


def test_check_room_availability_invalid_times():
    response = client.get(
        "/rooms/1/availability",
        params={"start": "2025-02-10T11:00:00", "end": "2025-02-10T10:00:00"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The start time must be earlier than the end time."
    }


def test_check_room_reservations(mock_db: MagicMock):
    mock_db.query.return_value.filter.return_value.first.return_value = Rooms(
        id=1,
        name="Room A",
        location="1st Floor",
        capacity=10,
        creator_id=1,
        created_at=date.today(),
    )
    mock_db.query.return_value.filter.return_value.count.return_value = 1
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
        Reservations(
            id=1,
            room_id=1,
            start_time=datetime(2025, 2, 10, 10, 0, 0),
            end_time=datetime(2025, 2, 10, 11, 0, 0),
        )
    ]

    response = client.get("/rooms/1/reservations?page=1&limit=10")

    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "limit": 10,
        "total_items": 1,
        "total_pages": 1,
        "reservations": [
            {
                "id": 1,
                "room_id": 1,
                "start_time": "2025-02-10T10:00:00",
                "end_time": "2025-02-10T11:00:00",
            }
        ],
    }


def test_create_room():
    room_data = {
        "name": "Room A",
        "location": "1st Floor",
        "capacity": 10,
        "creator_id": 1,
    }

    response = client.post("/rooms", json=room_data)

    assert response.status_code == 201
    assert "id" in response.json()
