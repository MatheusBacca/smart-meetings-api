import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import status
from database.database import get_db
from util.utils import create_app
from database.models import Users

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


def test_list_users_no_filters(mock_db: MagicMock):
    # Configura o mock para retornar uma lista de usuários
    mock_users = [
        Users(id=1, name="User1", email="user1@test.com"),
        Users(id=2, name="User2", email="user2@test.com"),
    ]
    mock_db.query.return_value.all.return_value = mock_users

    response = client.get("/users", params={})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "users": [
            {"id": 1, "name": "User1", "email": "user1@test.com"},
            {"id": 2, "name": "User2", "email": "user2@test.com"},
        ]
    }


def test_list_users_with_filters(mock_db: MagicMock):
    # Configura o mock para retornar um único usuário filtrado
    mock_users = [Users(id=1, name="FilteredUser", email="filtereduser@test.com")]
    mock_db.query.return_value.filter.return_value.all.return_value = mock_users

    response = client.get("/users", params={"name": "FilteredUser"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "users": [{"id": 1, "name": "FilteredUser", "email": "filtereduser@test.com"}]
    }


def test_create_user_success(mock_db: MagicMock):
    # Mock para garantir que o nome não exista no banco
    mock_db.query.return_value.filter.return_value.first.return_value = None
    user_request = {"name": "NewUser", "email": "newuser@test.com"}

    response = client.post("/users", json=user_request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == user_request["name"]
    assert response.json()["email"] == user_request["email"]


def test_create_user_conflict_name(mock_db: MagicMock):
    # Mock para retornar um usuário já existente com o mesmo nome
    mock_db.query.return_value.filter.return_value.first.return_value = Users(
        id=1, name="ExistingUser", email="existing@test.com"
    )
    user_request = {"name": "ExistingUser", "email": "newuser@test.com"}

    response = client.post("/users", json=user_request)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "User with name 'ExistingUser' already exists."
    }
