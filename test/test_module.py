from src.connections.pmongo import MainMongo
from src.routes.services.post import PostService
from src.models.post import PostSchema


def test_mongo_connection():
    mongo = MainMongo()
    try:
        mongo.connect()
        assert hasattr(mongo, "_client")
        assert mongo._client.admin.command("ismaster")
    finally:
        mongo.close()
        assert not hasattr(mongo, "_client")


def test_post_service():
    post_service = PostService()
    post = post_service.add_post(PostSchema(title="test", content="test"))
    assert post is not None

    post = post_service.get_post(post.id)
    assert post is not None

    count, _ = post_service.get_posts()
    assert count > 0

    post_id = post_service.update_post(
        post.id, PostSchema(title="test2", content="test2")
    )
    assert post_id == 1

    post = post_service.get_post(post.id)
    assert post is not None
    assert post.title == "test2"

    post_id = post_service.delete_post(post.id)
    assert post_id == 1
