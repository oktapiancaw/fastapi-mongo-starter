from redis.asyncio import Redis
from redis.exceptions import TimeoutError

from src.configs import LOGGER, CustomLogLevel
from src.models.connection import RedisConnectionMeta


class RedisConnector:

    _meta: RedisConnectionMeta
    _client: Redis

    def __init__(self, meta: RedisConnectionMeta) -> None:
        """
        Initialize the Redis connector with the given connection metadata.

        :param meta: The metadata of the database connection.
        :type meta: RedisConnectionMeta
        """
        self._meta = meta

    async def __enter__(self):
        """
        Connect to the Redis server and return the connection object.

        :return: The connection object.
        :rtype: RedisConnector
        :raises ValueError: If the connection to the Redis server fails.
        """
        await self.connect()
        if self._client is None:
            raise ValueError("Redis not connected.")
        return self

    async def __call__(self, *args, **kwds) -> bool:
        """
        Check if the connection is already established.

        :return: True if the connection is available, False otherwise.
        :rtype: bool
        """

        if self._client is None:
            raise ValueError("Redis not connected.")
        return True

    async def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Close the connection to the Redis server.

        This method is called when the context manager exits its scope.
        """
        await self.close()

    async def connect(self, other_database: int | None = None) -> None:
        """
        Establish a connection to the Redis server.

        :param other_database: The ID of an alternative database to connect to.
                               If not provided, the default database ID will be used.
        :type other_database: int | None
        :raises ValueError: If the connection to the Redis server fails.
        """
        try:

            self._client = await Redis(
                host=self._meta.host,  # type: ignore
                port=self._meta.port,  # type: ignore
                username=self._meta.username,
                password=self._meta.password,
                db=other_database if other_database else self._meta.database,  # type: ignore
            )

            LOGGER.log(CustomLogLevel.CONNECTION, "Redis connected.")
        except TimeoutError:
            raise ValueError("Redis connection timed out.")
        except Exception as e:
            raise e

    async def close(self) -> None:
        """
        Close the connection to the Redis server.

        This method is a no-op if the connection is already closed.
        """
        if self._client:
            await self._client.close()
        LOGGER.log(CustomLogLevel.CONNECTION, "Redis disconnected.")
