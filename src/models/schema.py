from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class OperateEnum(str, Enum):
    gt_ = "gt"
    lt_ = "lt"
    in_ = "in"
    nin_ = "nin"
    eq_ = "eq"
    regex_ = "regex"
    exist_ = "exist"


class FieldSearch(BaseModel):
    opt: Optional[OperateEnum] = Field(OperateEnum.eq_)
    field: str
    value: Optional[Any] = Field(None)


class SearchSchema(BaseModel):
    searchs: Optional[list[FieldSearch]] = []
    limit: Optional[int] = Field(10, gt=3, lte=100)
    page: Optional[int] = Field(1, gt=0)
    orderBy: Optional[str] = Field("created_at")
    order: Optional[int] = Field(1, gte=-1, lte=1)
