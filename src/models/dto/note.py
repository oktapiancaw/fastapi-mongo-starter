from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field, RootModel


class NoteType(str, Enum):
    MANUAL_BREW_NOTE = "manual-brew-note"
    COLD_BREW_NOTE = "cold-brew-note"
    REVIEW_NOTE = "review-note"


class NoteDetail(BaseModel):
    data: Optional[str] = None
    rating: Optional[int] = Field(0)


class BrewNoteDetail(NoteDetail):
    aroma: Optional[int] = Field(0)
    body: Optional[int] = Field(0)
    flavour: Optional[int] = Field(0)
    taste_note: Optional[list[str]] = Field([])


class PlaceNoteDetail(NoteDetail):
    ambience: Optional[int] = Field(0)
    design: Optional[int] = Field(0)
    hospitality: Optional[int] = Field(0)


class NoteSchema(BaseModel):
    name: str
    type: NoteType
    target_id: str
    detail: Union[NoteDetail, BrewNoteDetail, PlaceNoteDetail]


class Note(NoteSchema):
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


class Notes(RootModel):
    def __init__(self, notes: list[Note]):
        self._notes = notes

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
