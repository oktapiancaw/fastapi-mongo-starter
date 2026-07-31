from src.configs import LOGGER
from src.connections.pmongo import MainMongo
from src.models.dto.championship import (
    Championship,
    Championships,
    ChampionshipSchema,
)
from src.models.schema import SearchSchema


class ChampionshipService:
    # ? name of collection in mongo
    collection_name: str

    def __init__(self, collection_name: str = "championship") -> None:
        self.mongo = MainMongo()
        self.collection_name = collection_name

    def get_championship(self, id: str) -> Championship | None:
        """
        Get championship by id.

        :param id: The id of the championship.
        :return: The championship object if found, else None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            if raw := self.mongo._db[self.collection_name].find_one(
                {"_id": id}
            ):
                return Championship.model_validate(raw)
            return None
        except Exception:
            LOGGER.exception("Failed get championship")
            raise
        finally:
            self.mongo.close()

    def get_championships(
        self, query: dict = {}, filter: dict = {}
    ) -> tuple[int, Championships | None]:
        """
        Get multiple championships based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the championships object.
                 If no documents are found, the championships object will be None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            count = self.mongo._db[self.collection_name].count_documents(query)

            if raws := self.mongo._db[self.collection_name].find(query, filter):
                return count, Championships.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get championships")
            raise
        finally:
            self.mongo.close()

    def search_championships(
        self, searchs: SearchSchema
    ) -> tuple[int, Championships | None]:
        """
        Get multiple championships based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the championships object.
                 If no documents are found, the championships object will be None.
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
                return count, Championships.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get championships")
            raise
        finally:
            self.mongo.close()

    def add_championship(self, data: ChampionshipSchema) -> Championship:
        """
        Add a new championship to the collection.

        :param data: The data of the championship to be added.
        :type data: ChampionshipSchema
        :return: The added championship.
        :type: Championship
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = Championship.model_validate(data.model_dump())
            self.mongo._db[self.collection_name].insert_one(
                payload.model_dump(by_alias=True)
            )
            return payload
        except Exception:
            LOGGER.exception("Failed add championship")
            raise
        finally:
            self.mongo.close()

    def update_championship(self, id: str, data: ChampionshipSchema) -> int:
        """
        Update an existing championship in the collection.

        :param id: The id of the championship to be updated.
        :param data: The data to update the championship with.
        :type data: ChampionshipSchema
        :return: The number of documents modified (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = Championship.model_validate(data.model_dump())
            res = self.mongo._db[self.collection_name].update_one(
                {"_id": id}, {"$set": payload.updated_json}
            )

            return res.modified_count
        except Exception:
            LOGGER.exception("Failed update championship")
            raise
        finally:
            self.mongo.close()

    def delete_championship(self, id: str) -> int:
        """
        Delete an existing championship from the collection.

        :param id: The id of the championship to be deleted.
        :return: The number of documents deleted (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()
            res = self.mongo._db[self.collection_name].delete_one({"_id": id})
            return res.deleted_count
        except Exception:
            LOGGER.exception("Failed delete championship")
            raise
        finally:
            self.mongo.close()
