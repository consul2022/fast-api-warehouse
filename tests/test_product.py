import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app)as c:
        yield c


@pytest.fixture
def create_product(client):  # тест на создаение продукта
    response = client.post("/products",
                           json={"name": "Тестовый продукт", "description": "Тест продукта", "price": 100, "stock": 10})
    return response

def test_create_product(client, create_product):
    assert create_product.status_code == 200
    assert create_product.json()["name"] == "Тестовый продукт"


def test_get_product(client, create_product):
    product_id = create_product.json()['id']
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Тестовый продукт"


def test_delete_product(client, create_product):
    product_id = create_product.json()['id']
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404

