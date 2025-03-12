from datetime import datetime
from uuid import uuid4

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RequestTokenSchema(BaseModel):
    name: str
    email: EmailStr
    job: str
    institution: str
    purpose: str


class RequestToken(RequestTokenSchema):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    token: str
    createdAt: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000), ge=0
    )


class RequestTokenExtract(RequestTokenSchema):
    exp: Optional[int]
