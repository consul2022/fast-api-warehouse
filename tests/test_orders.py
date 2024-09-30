import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import OrderStatus


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_order(client):  # тест на создаение продукта
    create_product = client.post("/products",
                           json={"name": "Тестовый продукт", "description": "Тест продукта", "price": 100, "stock": 10})

    product_id = create_product.json()['id']
    response = client.post("/orders", json={"date": "2023-09-30T00:00:00", "status": "в процессе",
                                            "items": [{"product_id": product_id, "quantity": 2}]})
    return response


@pytest.fixture
def create_order_over_stock(client):  # тест на создаение продукта
    create_product = client.post("/products",
                                 json={"name": "Тестовый продукт", "description": "Тест продукта", "price": 100,
                                       "stock": 10})

    product_id = create_product.json()['id']
    response = client.post("/orders", json={"date": "2023-09-30T00:00:00", "status": "в процессе",
                                            "items": [{"product_id": product_id, "quantity": 12}]})
    return response


def test_create_order(client, create_order):
    assert create_order.status_code == 200
    assert create_order.json()["status"] == "в процессе"


def test_create_order_over_stock(client, create_order_over_stock):
    assert create_order_over_stock.status_code == 400


def test_update_order_status(client, create_order):
    order_id = create_order.json()['id']
    response = client.patch(f"/orders/{order_id}/status?status=доставлен")
    assert response.status_code == 200
    assert response.json()["status"] == "доставлен"


def test_get_order(client, create_order):
    order_id = create_order.json()['id']
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "в процессе"



