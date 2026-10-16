import allure
import pytest

from src.api.models import Post

pytestmark = pytest.mark.api


@allure.title("GET /posts/1 возвращает пост по схеме")
def test_get_post(api):
    response = api.get("/posts/1")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert Post(**response.json()).id == 1


@allure.title("GET /posts возвращает 100 постов, все по схеме")
def test_get_posts_list(api):
    response = api.get("/posts")

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 100
    for item in posts:
        Post(**item)


@allure.title("GET /posts?userId=1 возвращает только посты этого пользователя")
def test_filter_posts_by_user(api):
    response = api.get("/posts", params={"userId": 1})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 10
    assert all(post["userId"] == 1 for post in posts)


@allure.title("GET /posts/{post_id} возвращает пост с тем же id")
@pytest.mark.parametrize("post_id", [1, 2, 10, 50, 100])
def test_get_post_by_id(api, post_id):
    response = api.get(f"/posts/{post_id}")

    assert response.status_code == 200
    assert response.json()["id"] == post_id


@allure.title("GET несуществующего поста возвращает 404")
@pytest.mark.parametrize("post_id", [0, -1, 999999])
def test_get_missing_post(api, post_id):
    response = api.get(f"/posts/{post_id}")

    assert response.status_code == 404


@allure.title("POST /posts создаёт пост")
def test_create_post(api):
    payload = {"title": "Python QA", "body": "Testing POST", "userId": 1}

    response = api.post("/posts", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data


@allure.title("PUT /posts/1 полностью обновляет пост")
def test_update_post(api):
    payload = {"id": 1, "title": "Updated", "body": "Testing PUT", "userId": 1}

    response = api.put("/posts/1", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


@allure.title("PATCH /posts/1 частично обновляет пост")
def test_patch_post(api):
    response = api.patch("/posts/1", json={"title": "Patched"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Patched"
    assert data["id"] == 1
    assert data["userId"] == 1


@allure.title("DELETE /posts/1 удаляет пост")
def test_delete_post(api):
    response = api.delete("/posts/1")

    assert response.status_code == 200
