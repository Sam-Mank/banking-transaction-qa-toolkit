
import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def post_response():
    return requests.get(f"{BASE_URL}/posts/1", timeout=10)


def test_api_returns_200(post_response):
    assert post_response.status_code == 200


def test_response_contains_correct_post_id(post_response):
    assert post_response.json()["id"] == 1


def test_response_contains_title(post_response):
    assert post_response.json()["title"]


def test_response_contains_correct_user_id(post_response):
    assert post_response.json()["userId"] == 1


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_multiple_posts_return_correct_id(post_id):
    response = requests.get(
        f"{BASE_URL}/posts/{post_id}",
        timeout=10
    )

    assert response.status_code == 200
    assert response.json()["id"] == post_id
