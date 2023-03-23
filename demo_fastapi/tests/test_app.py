import requests


def test_app_live():
    response = requests.get("http://127.0.0.1:8000/livez")
    assert response.status_code == 200


def test_app_ready():
    response = requests.get("http://127.0.0.1:8000/readyz")
    assert response.status_code == 200


def test_brand_list():
    response = requests.get("http://127.0.0.1:8000/api/v1/brands/list")
    assert response.status_code == 200


def test_get_brand():
    response = requests.get("http://127.0.0.1:8000/api/v1/brands/4")
    assert response.status_code == 200
