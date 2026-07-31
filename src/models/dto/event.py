from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class EventSchema(BaseModel):
    title: str
    type: str
    place: str
    place_google_map: Optional[str] = ""
    description: Optional[str] = ""

    start_date: int
    end_date: int

    sponsorships: Optional[list[str]] = []

    model_config = ConfigDict(
        extra="forbid",
    )


class Event(EventSchema):
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


class Events(RootModel):
    def __init__(self, events: list[Event]):
        self._events = events

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
