from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class ReferenceTaste(BaseModel):
    reference: str
    aroma: Optional[int] = Field(None)
    aroma_preparation: Optional[str] = Field(None)
    flavour: Optional[int] = Field(None)
    flavour_preparation: Optional[str] = Field(None)


class TasteNoteSchema(BaseModel):
    name: str
    parent_id: Optional[str] = Field(None)
    grandparent_id: Optional[str] = Field(None)
    colour: str
    icon: Optional[str] = Field(None)
    definition: str
    references: Optional[list[ReferenceTaste]] = []

    model_config = ConfigDict(
        extra="forbid",
    )


class TasteNote(TasteNoteSchema):
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


class TasteNotes(RootModel):
    def __init__(self, taste_notes: list[TasteNote]):
        self._taste_notes = taste_notes

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
