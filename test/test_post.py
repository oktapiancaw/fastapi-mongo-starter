from fastapi.testclient import TestClient

from src.main import app
from src.models.post import Post, PostSchema


client = TestClient(app)


SAMPLE = [
    PostSchema(
        title="Data Science",
        content="Some content",
        published=True,
    ),
    PostSchema(
        title="Data Analyst",
        content="Some content",
        published=True,
    ),
]


# * Create -> Get One -> Delete
def test_creation_post():
    # ? Create Post
    """
    Test a complete flow of creating a post, getting the post, and then deleting the post.

    1. Create Post: POST /posts
    2. Get Post: GET /posts/<id>
    3. Delete Post: DELETE /posts/<id>
    """
    response = client.post(
        "/posts",
        json=SAMPLE[0].model_dump(by_alias=True),
    )
    assert response.status_code == 201
    assert Post.model_validate(response.json().get("data"))
    payload = response.json().get("data")

    # ? Get Post
    response = client.get(f"/posts/{payload.get('_id')}")
    assert response.status_code == 200
    assert response.json().get("data").get("title") == SAMPLE[0].title
    assert Post.model_validate(response.json().get("data"))

    # ? Delete Post
    response = client.delete(f"/posts/{payload.get('_id')}")
    assert response.status_code == 200


# * Create -> Get all -> Delete -> Get all
def test_multiple_post():
    # ? Create Post
    """
    Test multiple posts flow.

    1. Create Post: POST /posts
    2. Get all Posts: GET /posts
    3. Delete Post: DELETE /posts/<id>
    4. Get all Posts: GET /posts
    """
    response = client.post(
        "/posts",
        json=SAMPLE[0].model_dump(by_alias=True),
    )
    assert response.status_code == 201
    assert Post.model_validate(response.json().get("data"))
    payload = response.json().get("data")

    # ? Get all Post
    response = client.get(f"/posts")
    assert response.status_code == 200
    total = response.json().get("total")

    # ? Delete Post
    response = client.delete(f"/posts/{payload.get('_id')}")
    assert response.status_code == 200

    # ? Get all Post
    response = client.get(f"/posts")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.json().get("total") != total


# * Create -> Update -> Get One -> Delete
def test_update_post():
    # ? Create Post
    """
    Test update post flow.

    1. Create Post: POST /posts
    2. Update Post: PUT /posts/<id>
    3. Get Post: GET /posts/<id>
    4. Delete Post: DELETE /posts/<id>
    """
    response = client.post(
        "/posts",
        json=SAMPLE[0].model_dump(by_alias=True),
    )
    assert response.status_code == 201
    assert Post.model_validate(response.json().get("data"))
    payload = response.json().get("data")

    # ? Update Post
    response = client.put(
        f"/posts/{payload.get('_id')}",
        json=SAMPLE[1].model_dump(by_alias=True),
    )
    assert response.status_code == 200
    assert response.json().get("id") == payload.get("_id")

    # ? Get Post
    response = client.get(f"/posts/{payload.get('_id')}")
    assert response.status_code == 200
    assert response.json().get("data").get("title") != SAMPLE[0].title
    assert response.json().get("data").get("title") == SAMPLE[1].title
    assert Post.model_validate(response.json().get("data"))

    # ? Delete Post
    response = client.delete(f"/posts/{payload.get('_id')}")
    assert response.status_code in [200, 404]
