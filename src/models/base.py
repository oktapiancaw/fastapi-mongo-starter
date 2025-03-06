from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ApplicationStage(str, Enum):
    DEV = "dev"
    PROD = "prod"


class ApplicationMeta(BaseModel):
    port: int = Field(8001)
    host: str = Field("0.0.0.0")
    stage: ApplicationStage = Field(ApplicationStage.DEV)
    workers: Optional[int] = Field(1)
