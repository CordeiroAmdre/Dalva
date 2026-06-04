from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field


class ChatDalvaRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    tenant_id: str | None = None


class ChartSpec(BaseModel):
    """Full Apache ECharts option object passed through to the frontend."""

    option: dict[str, Any]


class ChatDalvaResponse(BaseModel):
    reply: str
    model: str
    used_database: bool = False
    data_sources: list[str] = Field(default_factory=list)
    chart: ChartSpec | None = None


@dataclass
class AgentResult:
    """Internal result from the SQL agent orchestration layer."""

    reply: str
    used_database: bool = False
    data_sources: list[str] = field(default_factory=list)
    iterations: int = 0
