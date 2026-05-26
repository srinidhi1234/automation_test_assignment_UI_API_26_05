import pytest
import requests


def test_get_posts_returns_posts_with_required_fields(
    api_session, jsonplaceholder_base_url
):
    response = api_session.get(f"{jsonplaceholder_base_url}/posts")

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert posts, "Expected at least one post"

    required_fields = {"id", "title", "body", "userId"}
    for post in posts:
        assert required_fields.issubset(post)
        assert isinstance(post["id"], int)
        assert isinstance(post["userId"], int)
        assert post["title"]
        assert post["body"]


def test_get_single_post_has_correct_shape_and_non_empty_values(
    api_session, jsonplaceholder_base_url
):
    response = api_session.get(f"{jsonplaceholder_base_url}/posts/1")

    assert response.status_code == 200
    post = response.json()
    assert set(post) == {"userId", "id", "title", "body"}
    assert post["id"] == 1
    assert isinstance(post["userId"], int)
    assert post["title"].strip()
    assert post["body"].strip()


def test_get_unknown_post_returns_404(api_session, jsonplaceholder_base_url):
    response = api_session.get(f"{jsonplaceholder_base_url}/posts/99999")

    assert response.status_code == 404


def test_create_post_returns_created_payload(api_session, jsonplaceholder_base_url):
    payload = {
        "title": "automated test title",
        "body": "created by the pytest API suite",
        "userId": 42,
    }

    response = api_session.post(f"{jsonplaceholder_base_url}/posts", json=payload)

    assert response.status_code == 201
    created_post = response.json()
    for field, value in payload.items():
        assert created_post[field] == value
    assert isinstance(created_post["id"], int)


def test_update_post_reflects_changes(api_session, jsonplaceholder_base_url):
    payload = {
        "id": 1,
        "title": "updated automated title",
        "body": "updated body from the test suite",
        "userId": 7,
    }

    response = api_session.put(f"{jsonplaceholder_base_url}/posts/1", json=payload)

    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post == payload


def test_delete_post_returns_success(api_session, jsonplaceholder_base_url):
    response = api_session.delete(f"{jsonplaceholder_base_url}/posts/1")

    assert response.status_code == 200
    assert response.json() == {}


def test_filter_posts_by_user_id(api_session, jsonplaceholder_base_url):
    response = api_session.get(f"{jsonplaceholder_base_url}/posts", params={"userId": 1})

    assert response.status_code == 200
    posts = response.json()
    assert posts, "Expected userId=1 to have posts"
    assert all(post["userId"] == 1 for post in posts)


def test_post_comments_have_non_empty_email(api_session, jsonplaceholder_base_url):
    response = api_session.get(f"{jsonplaceholder_base_url}/posts/1/comments")

    assert response.status_code == 200
    comments = response.json()
    assert comments, "Expected post 1 to have comments"
    for comment in comments:
        assert "email" in comment
        assert comment["email"].strip()
        assert "@" in comment["email"]


def test_httpbin_500_is_handled_without_crashing(api_session, httpbin_base_url):
    response = api_session.get(f"{httpbin_base_url}/status/500")

    assert response.status_code == 500


def test_httpbin_delay_request_raises_timeout(api_session, httpbin_base_url):
    with pytest.raises(requests.exceptions.Timeout):
        api_session.get(f"{httpbin_base_url}/delay/3", timeout=2)
