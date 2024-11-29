from uuid import uuid4
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, RootModel, Field, ConfigDict


class PostSchema(BaseModel):
    title: str = Field(..., description="Title post")
    content: str = Field(..., description="Content post")
    published: Optional[bool] = Field(default=True, description="Published post")

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "Title post",
                "content": "Content post",
                "published": True,
            }
        },
    )


class Post(PostSchema):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    status: Optional[str] = "active"
    createdAt: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000), ge=0
    )
    updatedAt: Optional[int] = Field(None)

    @property
    def updated_json(self):
        self.updatedAt = int(datetime.now().timestamp() * 1000)
        return self.model_dump(by_alias=True, exclude={"id", "createdAt"})


class Posts(RootModel):
    root: list[Post]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return self.root.__len__()
