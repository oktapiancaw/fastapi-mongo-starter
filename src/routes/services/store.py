from src.configs import LOGGER
from src.connections.pmongo import MainMongo
from src.models.dto.store import Store, Stores, StoreSchema
from src.models.schema import SearchSchema


class StoreService:
    # ? name of collection in mongo
    collection_name: str

    def __init__(self, collection_name: str = "store") -> None:
        self.mongo = MainMongo()
        self.collection_name = collection_name

    def get_store(self, id: str) -> Store | None:
        """
        Get store by id.

        :param id: The id of the store.
        :return: The store object if found, else None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            if raw := self.mongo._db[self.collection_name].find_one(
                {"_id": id}
            ):
                return Store.model_validate(raw)
            return None
        except Exception:
            LOGGER.exception("Failed get store")
            raise
        finally:
            self.mongo.close()

    def get_stores(
        self, query: dict = {}, filter: dict = {}
    ) -> tuple[int, Stores | None]:
        """
        Get multiple stores based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the stores object.
                 If no documents are found, the stores object will be None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            count = self.mongo._db[self.collection_name].count_documents(query)

            if raws := self.mongo._db[self.collection_name].find(query, filter):
                return count, Stores.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get stores")
            raise
        finally:
            self.mongo.close()

    def search_stores(self, searchs: SearchSchema) -> tuple[int, Stores | None]:
        """
        Get multiple stores based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the stores object.
                 If no documents are found, the stores object will be None.
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
                return count, Stores.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get stores")
            raise
        finally:
            self.mongo.close()

    def add_store(self, data: StoreSchema) -> Store:
        """
        Add a new store to the collection.

        :param data: The data of the store to be added.
        :type data: StoreSchema
        :return: The added store.
        :type: Store
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = Store.model_validate(data.model_dump())
            self.mongo._db[self.collection_name].insert_one(
                payload.model_dump(by_alias=True)
            )
            return payload
        except Exception:
            LOGGER.exception("Failed add store")
            raise
        finally:
            self.mongo.close()

    def update_store(self, id: str, data: StoreSchema) -> int:
        """
        Update an existing store in the collection.

        :param id: The id of the store to be updated.
        :param data: The data to update the store with.
        :type data: StoreSchema
        :return: The number of documents modified (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = Store.model_validate(data.model_dump())
            res = self.mongo._db[self.collection_name].update_one(
                {"_id": id}, {"$set": payload.updated_json}
            )

            return res.modified_count
        except Exception:
            LOGGER.exception("Failed update store")
            raise
        finally:
            self.mongo.close()

    def delete_store(self, id: str) -> int:
        """
        Delete an existing store from the collection.

        :param id: The id of the store to be deleted.
        :return: The number of documents deleted (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()
            res = self.mongo._db[self.collection_name].delete_one({"_id": id})
            return res.deleted_count
        except Exception:
            LOGGER.exception("Failed delete store")
            raise
        finally:
            self.mongo.close()
