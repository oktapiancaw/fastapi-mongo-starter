from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class FarmLocationDetail(BaseModel):
    city: Optional[str] = None
    province: Optional[str] = None
    country: str
    continent: str


class BeanSchema(BaseModel):
    title: str
    tags: list[str]
    description: Optional[str] = None
    flavour_type: Optional[list[str]] = []
    taste_notes: list[str]
    variety: list[str]
    process: list[str]
    roast_profile: str
    farm_location: Optional[str] = None
    farm_altitude: Optional[int] = None
    farm_name: Optional[str] = None
    product_link: str
    shop: str
    blend: Optional[bool] = False

    model_config = ConfigDict(
        extra="forbid",
    )


class Bean(BeanSchema):
    # ? Meta
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    status: Optional[str] = "active"
    farm_location_detail: FarmLocationDetail
    sca_taste_notes: list[str]

    # ? Generated
    updated_at: Optional[int] = Field(None)
    created_at: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000), ge=0
    )

    @property
    def updated_json(self):
        self.updatedAt = int(datetime.now().timestamp() * 1000)
        return self.model_dump(by_alias=True, exclude={"id", "created_at"})


class Beans(RootModel):
    def __init__(self, beans: list[Bean]):
        self._beans = beans

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
