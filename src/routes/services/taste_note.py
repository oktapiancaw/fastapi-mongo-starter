from src.configs import LOGGER
from src.connections.pmongo import MainMongo
from src.models.dto.taste_note import TasteNote, TasteNotes, TasteNoteSchema
from src.models.schema import SearchSchema


class TasteNoteService:
    # ? name of collection in mongo
    collection_name: str

    def __init__(self, collection_name: str = "taste_note") -> None:
        self.mongo = MainMongo()
        self.collection_name = collection_name

    def get_taste_note(self, id: str) -> TasteNote | None:
        """
        Get taste_note by id.

        :param id: The id of the taste_note.
        :return: The taste_note object if found, else None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            if raw := self.mongo._db[self.collection_name].find_one(
                {"_id": id}
            ):
                return TasteNote.model_validate(raw)
            return None
        except Exception:
            LOGGER.exception("Failed get taste note")
            raise
        finally:
            self.mongo.close()

    def get_taste_notes(
        self, query: dict = {}, filter: dict = {}
    ) -> tuple[int, TasteNotes | None]:
        """
        Get multiple taste_notes based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the taste_notes object.
                 If no documents are found, the taste_notes object will be None.
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            count = self.mongo._db[self.collection_name].count_documents(query)

            if raws := self.mongo._db[self.collection_name].find(query, filter):
                return count, TasteNotes.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get taste notes")
            raise
        finally:
            self.mongo.close()

    def search_taste_notes(
        self, searchs: SearchSchema
    ) -> tuple[int, TasteNotes | None]:
        """
        Get multiple taste_notes based on a query

        :param query: The query to filter documents in the collection.
        :param filter: The filter which fields to retrieve,
        :return: A tuple containing the count of documents and the taste_notes object.
                 If no documents are found, the taste_notes object will be None.
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
                return count, TasteNotes.model_validate(raws.to_list())
            return count, None

        except Exception:
            LOGGER.exception("Failed get taste notes")
            raise
        finally:
            self.mongo.close()

    def add_taste_note(self, data: TasteNoteSchema) -> TasteNote:
        """
        Add a new taste_note to the collection.

        :param data: The data of the taste_note to be added.
        :type data: TasteNoteSchema
        :return: The added taste_note.
        :type: TasteNote
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = TasteNote.model_validate(data.model_dump())
            self.mongo._db[self.collection_name].insert_one(
                payload.model_dump(by_alias=True)
            )
            return payload
        except Exception:
            LOGGER.exception("Failed add taste note")
            raise
        finally:
            self.mongo.close()

    def update_taste_note(self, id: str, data: TasteNoteSchema) -> int:
        """
        Update an existing taste_note in the collection.

        :param id: The id of the taste_note to be updated.
        :param data: The data to update the taste_note with.
        :type data: TasteNoteSchema
        :return: The number of documents modified (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()

            payload = TasteNote.model_validate(data.model_dump())
            res = self.mongo._db[self.collection_name].update_one(
                {"_id": id}, {"$set": payload.updated_json}
            )

            return res.modified_count
        except Exception:
            LOGGER.exception("Failed update taste note")
            raise
        finally:
            self.mongo.close()

    def delete_taste_note(self, id: str) -> int:
        """
        Delete an existing taste_note from the collection.

        :param id: The id of the taste_note to be deleted.
        :return: The number of documents deleted (0 if no document with the given id is found).
        :raises: Exception if any error occurs during the process.
        """
        try:
            self.mongo.connect()
            res = self.mongo._db[self.collection_name].delete_one({"_id": id})
            return res.deleted_count
        except Exception:
            LOGGER.exception("Failed delete taste note")
            raise
        finally:
            self.mongo.close()
