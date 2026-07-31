from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, RootModel


class ChampionshipLevel(str, Enum):
    INTERNATIONAL = "international"
    NATIONAL = "national"
    PROVINCE = "province"
    CITY = "city"
    REGIONAL = "regional"


class ChampionMeta(BaseModel):
    person_id: str
    rank: str
    title_persentation: Optional[str] = None
    detail_persentation: Optional[str] = None
    score: Optional[float] = 0


class ChampionshipSchema(BaseModel):
    title: str
    level: ChampionshipLevel
    champions: list[ChampionMeta]
    year: int
    start_date: int
    end_date: int

    model_config = ConfigDict(
        extra="forbid",
    )


class Championship(ChampionshipSchema):
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


class Championships(RootModel):
    def __init__(self, championships: list[Championship]):
        self._championships = championships

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
