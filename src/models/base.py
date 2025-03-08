from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ApplicationStage(str, Enum):
    DEV = "dev"
    PROD = "prod"


class ApplicationMeta(BaseModel):
    stage: ApplicationStage = Field(ApplicationStage.DEV)
    workers: Optional[int] = Field(1)
