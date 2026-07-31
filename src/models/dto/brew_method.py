from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class ScheduleMeta(BaseModel):
    id: int
    time: int
    endTime: int
    volume: int
    label: Optional[str] = None


class BrewMethodSchema(BaseModel):
    title: str
    creator: Optional[str] = ""
    tags: Optional[list[str]] = []
    coffeeGram: int
    grindSize: str
    roastLevel: str
    waterTemp: int
    schedules: list[ScheduleMeta]

    model_config = ConfigDict(
        extra="forbid",
    )


class BrewMethod(BrewMethodSchema):
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


class BrewMethods(RootModel):
    def __init__(self, brew_methods: list[BrewMethod]):
        self._brew_methods = brew_methods

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
