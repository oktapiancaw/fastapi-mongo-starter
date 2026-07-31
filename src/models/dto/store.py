from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class StoreSchema(BaseModel):
    name: str
    type: list[str]
    description: Optional[str] = None
    owners: Optional[list[str]] = []
    operational_google_map: Optional[str] = None
    operational_address: Optional[str] = None
    operational_hours: Optional[list[str]] = []
    online_shop_links: Optional[list[str]] = []
    personal_profile: Optional[str] = None
    model_config = ConfigDict(
        extra="forbid",
    )


class Store(StoreSchema):
    # ? Meta
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    status: Optional[str] = "active"
    slug: Optional[str] = Field(None)

    # ? Generated
    updated_at: Optional[int] = Field(None)
    created_at: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000), ge=0
    )

    @property
    def updated_json(self):
        self.updatedAt = int(datetime.now().timestamp() * 1000)
        return self.model_dump(by_alias=True, exclude={"id", "created_at"})


class Stores(RootModel):
    def __init__(self, stores: list[Store]):
        self._stores = stores

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
