from src.configs import logger
from src.models.post import Posts, Post, PostSchema
from src.connections.pmongo import MainMongo


class PostService:

    # ? name of collection in mongo
    collection_name: str

    def __init__(self, collection_name: str = "post") -> None:
        self.mongo = MainMongo()
        self.collection_name = collection_name

    def get_post(self, id: str) -> Post | None:
        """
        Get post by id.

        :param id: The id of the post.
        :return: The post object if found, else None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            if raw := self.mongo._db[self.collection_name].find_one({"_id": id}):
                return Post.model_validate(raw)
            return None
        except Exception:
            logger.exception("Failed get post")
            raise
        finally:
            self.mongo.close()

    def get_posts(
        self, query: dict = {}, filter: dict = {}
    ) -> tuple[int, Posts | None]:
        """
        Get multiple posts based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the posts object.
                 If no documents are found, the posts object will be None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            count = self.mongo._db[self.collection_name].count_documents(query)

            if raws := self.mongo._db[self.collection_name].find(query, filter):
                return count, Posts.model_validate(raws.to_list())
            return count, None

        except Exception:
            logger.exception("Failed get posts")
            raise
        finally:
            self.mongo.close()

    def add_post(self, data: PostSchema) -> Post:
        """
        Add a new post to the collection.

        :param data: The data of the post to be added.
        :type data: PostSchema
        :return: The added post.
        :type: Post
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = Post.model_validate(data.model_dump())
            self.mongo._db[self.collection_name].insert_one(
                payload.model_dump(by_alias=True)
            )
            return payload
        except Exception:
            logger.exception("Failed add post")
            raise
        finally:
            self.mongo.close()

    def update_post(self, id: str, data: PostSchema) -> int:
        """
        Update an existing post in the collection.

        :param id: The id of the post to be updated.
        :param data: The data to update the post with.
        :type data: PostSchema
        :return: The number of documents modified (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = Post.model_validate(data.model_dump())
            res = self.mongo._db[self.collection_name].update_one(
                {"_id": id}, {"$set": payload.updated_json}
            )

            return res.modified_count
        except Exception:
            logger.exception("Failed update post")
            raise
        finally:
            self.mongo.close()

    def delete_post(self, id: str) -> int:
        """
        Delete an existing post from the collection.

        :param id: The id of the post to be deleted.
        :return: The number of documents deleted (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()
            res = self.mongo._db[self.collection_name].delete_one({"_id": id})
            return res.deleted_count
        except Exception:
            logger.exception("Failed delete post")
            raise
        finally:
            self.mongo.close()
