from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class PersonSchema(BaseModel):
    name: str
    alias: Optional[list[str]] = []
    role: list[str]
    achievements: list[str] = []
    personal_profile: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid",
    )


class Person(PersonSchema):
    # ? Meta
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    status: Optional[str] = "active"

    # ? Generated
    updated_at: Optional[int] = Field(None)
    created_at: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000), ge=0
    )

    @property
    def updated_json(self):
        self.updatedAt = int(datetime.now().timestamp() * 1000)
        return self.model_dump(by_alias=True, exclude={"id", "created_at"})


class Persons(RootModel):
    def __init__(self, persons: list[Person]):
        self._persons = persons

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
