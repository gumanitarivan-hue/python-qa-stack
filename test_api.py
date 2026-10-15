import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_post_returns_200():
    response = requests.get(f"{BASE_URL}/posts/1", timeout=10)

    assert response.status_code == 200


def test_get_post_returns_expected_data():
    response = requests.get(f"{BASE_URL}/posts/1", timeout=10)
    data = response.json()

    assert data["userId"] == 1
    assert data["id"] == 1
    assert isinstance(data["title"], str)
    assert len(data["title"]) > 0


def test_get_missing_post_returns_404():
    response = requests.get(f"{BASE_URL}/posts/999999", timeout=10)

    assert response.status_code == 404


def test_get_posts_returns_list():
    response = requests.get(f"{BASE_URL}/posts", timeout=10)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

import pytest


@pytest.mark.parametrize(
    "post_id",
    [1, 2, 10, 50, 100],
)
def test_get_posts_by_id(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)

    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.parametrize(
    "invalid_post_id",
    [0, -1, 999999],
)
def test_get_invalid_post_ids(invalid_post_id):
    response = requests.get(
        f"{BASE_URL}/posts/{invalid_post_id}",
        timeout=10,
    )

    assert response.status_code == 404