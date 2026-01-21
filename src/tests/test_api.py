import pytest
import requests


BASE_URL = 'http://localhost:8080'

PRODUCTS = [
        ("product0", 0),
        ("product1", 10),
        ("product2", 20),
        ("product3", 30),
        ("product4", 40),
    ]

def test_health():
    response = requests.get(f"{BASE_URL}/get-health")
    assert response.status_code == 200 and response.json()["status"] == "healthy"

@pytest.mark.parametrize("name, quantity", PRODUCTS)
def test_create_stock(name: str, quantity: int) -> None:
    response = requests.post(
        url=f"{BASE_URL}/create-stock/{name}/{quantity}",
    )
    assert response.status_code == 200

def test_buy_in_stock(product: tuple = PRODUCTS[1]):
    response = requests.post(
        url=f"{BASE_URL}/buy-item/{product[0]}"
    )
    assert response.status_code == 200 and "sold out" not in response.json()["message"].lower()

def test_buy_not_in_stock(product: tuple = PRODUCTS[0]):
    response = requests.post(
        url=f"{BASE_URL}/buy-item/{product[0]}"
    )
    assert response.status_code == 200 and "sold out" in response.json()["message"].lower()

def test_buy_unknown(product: tuple = ("unknown_id", 0)):
    response = requests.post(
        url=f"{BASE_URL}/buy-item/{product[0]}"
    )
    assert response.status_code != 200

