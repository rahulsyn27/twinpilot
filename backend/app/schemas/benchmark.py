from typing import Any

from pydantic import BaseModel, Field


class BenchmarkRunRequest(BaseModel):
    plugin_id: str
    dataset_id: str = "starter-rag"
    top_k: int = Field(default=3, ge=1, le=10)


class BenchmarkRunResponse(BaseModel):
    id: str
    plugin_id: str
    dataset_id: str
    status: str
    result: dict[str, Any]
