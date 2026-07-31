from src.configs import LOGGER
from src.connections.pmongo import MainMongo
from src.models.dto.brew_method import BrewMethod, BrewMethods, BrewMethodSchema
from src.models.schema import SearchSchema


class BrewMethodService:
    # ? name of collection in mongo
    collection_name: str

    def __init__(self, collection_name: str = "brew_method") -> None:
        self.mongo = MainMongo()
        self.collection_name = collection_name

    def get_brew_method(self, id: str) -> BrewMethod | None:
        """
        Get brew_method by id.

        :param id: The id of the brew_method.
        :return: The brew_method object if found, else None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            if raw := self.mongo._db[self.collection_name].find_one(
                {"_id": id}
            ):
                return BrewMethod.model_validate(raw)
            return None
        except Exception:
            LOGGER.exception("Failed get brew method")
            raise
        finally:
            self.mongo.close()

    def get_brew_methods(
        self, query: dict = {}, filter: dict = {}
    ) -> tuple[int, BrewMethods | None]:
        """
        Get multiple brew_methods based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the brew_methods object.
                 If no documents are found, the brew_methods object will be None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            count = self.mongo._db[self.collection_name].count_documents(query)

            if raws := self.mongo._db[self.collection_name].find(query, filter):
                return count, BrewMethods.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get brew methods")
            raise
        finally:
            self.mongo.close()

    def search_brew_methods(
        self, searchs: SearchSchema
    ) -> tuple[int, BrewMethods | None]:
        """
        Get multiple brew_methods based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the brew_methods object.
                 If no documents are found, the brew_methods object will be None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            query = {}

            for search in searchs.searchs or []:
                if search.opt == "eq":
                    query.update({search.field: search.value})
                elif search.opt in ["gt", "lt", "in", "nin"]:
                    query.update(
                        {search.field: {f"${search.opt}": search.value}}
                    )
                elif search.opt == "regex":
                    query.update(
                        {
                            search.field: {
                                "$regex": search.value,
                                "$options": "i",
                            }
                        }
                    )
                elif search.opt == "exist":
                    query.update({search.field: {"$exist": 1}})

            count = self.mongo._db[self.collection_name].count_documents(query)

            # Pagination
            limit = searchs.limit or 10
            page = searchs.page or 1
            skip = (page - 1) * limit
            if (
                raws := self.mongo._db[self.collection_name]
                .find(query)
                .sort(searchs.orderBy or "created_at", searchs.order or 1)
                .skip(skip)
                .limit(limit)
            ):
                return count, BrewMethods.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get brew methods")
            raise
        finally:
            self.mongo.close()

    def add_brew_method(self, data: BrewMethodSchema) -> BrewMethod:
        """
        Add a new brew_method to the collection.

        :param data: The data of the brew_method to be added.
        :type data: BrewMethodSchema
        :return: The added brew_method.
        :type: BrewMethod
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = BrewMethod.model_validate(data.model_dump())
            self.mongo._db[self.collection_name].insert_one(
                payload.model_dump(by_alias=True)
            )
            return payload
        except Exception:
            LOGGER.exception("Failed add brew method")
            raise
        finally:
            self.mongo.close()

    def update_brew_method(self, id: str, data: BrewMethodSchema) -> int:
        """
        Update an existing brew_method in the collection.

        :param id: The id of the brew_method to be updated.
        :param data: The data to update the brew_method with.
        :type data: BrewMethodSchema
        :return: The number of documents modified (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = BrewMethod.model_validate(data.model_dump())
            res = self.mongo._db[self.collection_name].update_one(
                {"_id": id}, {"$set": payload.updated_json}
            )

            return res.modified_count
        except Exception:
            LOGGER.exception("Failed update brew method")
            raise
        finally:
            self.mongo.close()

    def delete_brew_method(self, id: str) -> int:
        """
        Delete an existing brew_method from the collection.

        :param id: The id of the brew_method to be deleted.
        :return: The number of documents deleted (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()
            res = self.mongo._db[self.collection_name].delete_one({"_id": id})
            return res.deleted_count
        except Exception:
            LOGGER.exception("Failed delete brew method")
            raise
        finally:
            self.mongo.close()
