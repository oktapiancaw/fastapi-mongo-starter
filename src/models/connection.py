import re
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class EndpointMeta(BaseModel):
    host: Optional[str] = Field("localhost", description="Connection host")
    port: Optional[str | int] = Field(8000, description="Connection port")


class AuthMeta(BaseModel):
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")


class URIConnectionMeta(BaseModel):
    uri: Optional[str] = Field("", description="Database connection URI")


class DBConnectionMeta(EndpointMeta, AuthMeta, URIConnectionMeta):
    database: Optional[str] = Field(None, description="Database name")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        """
        Return a URI string for the database connection.

        :param base: The base of the URI (e.g. "http", "postgresql", etc.).
        :param with_db: Whether to include the database name in the URI.
        :return: A string representing the URI.
        """
        if self.host:
            meta = f"{self.host}:{self.port}"
            if self.username:
                return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db else ''}"
            return f"{base}://{meta}/{self.database if with_db else ''}"
        return ""

    @model_validator(mode="after")
    def extract_uri(self):
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and "&" in others:
                for other in others.split("&"):
                    if "=" in other and re.search(r"authSource", other):
                        self.database = other.split("=")[-1]
                    elif "=" not in other:
                        self.database = other
            if "@" in metadata:
                self.username, self.password, self.host, self.port = re.split(
                    r"\@|\:", metadata
                )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            if self.port:
                self.port = int(self.port)
        return self
