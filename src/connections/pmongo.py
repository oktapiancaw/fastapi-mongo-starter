from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import NetworkTimeout, ExecutionTimeout

from src.configs import config
from src.models.connection import DBConnectionMeta


class MongoConnector:

    _meta: DBConnectionMeta
    _client: MongoClient
    _db: Database

    def __init__(self, meta: DBConnectionMeta) -> None:
        """
        Initialize the Mongo connector with the given connection metadata.

        :param meta: The metadata of the database connection.
        :type meta: DBConnectionMeta
        """
        self._meta = meta
        if not self._meta.uri:
            self._meta.uri = self._meta.uri_string(base="mongodb", with_db=False)

    def __enter__(self):
        """
        Connect to the MongoDB server and return the connection object.

        :return: The connection object.
        :rtype: MongoConnector
        :raises ValueError: If the connection to the MongoDB server fails.
        """
        self.connect()
        if self._client is None:
            raise ValueError("Mongo not connected.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Close the connection to the MongoDB server.

        This method is called when the context manager exits its scope.
        """
        self.close()

    def connect(self, **kwargs) -> None:
        """
        Establish a connection to the MongoDB server.

        :param kwargs: Additional keyword arguments for MongoClient.
        :raises ValueError: If the connection to the MongoDB server fails.
        :raises Exception: If any other error occurs during the connection.
        """

        try:
            self._client = MongoClient(self._meta.uri, timeoutMS=20000, **kwargs)
            self._db = self._client[str(self._meta.database)]
        except (NetworkTimeout, ExecutionTimeout):
            raise ValueError("Mongo connection timed out.")
        except Exception as e:
            raise e

    def close(self) -> None:
        """
        Close the connection to the MongoDB server.

        This method is a no-op if the connection is already closed.
        """
        if self._client:
            self._client.close()
            self.__delattr__("_client")


class MainMongo(MongoConnector):
    def __init__(self):
        super().__init__(meta=config.mongo)
