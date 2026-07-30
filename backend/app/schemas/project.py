from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class ProjectCreate(BaseModel):
    name: str
    repository_url: HttpUrl
    local_path: str
    default_branch: str = "main"


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    repository_url: str
    local_path: str
    default_branch: str

    created_at: datetime
    updated_at: datetime