from dataclasses import dataclass, field

from pydantic import BaseModel, Field


class ChatDalvaRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatDalvaResponse(BaseModel):
    reply: str
    model: str
    used_database: bool = False
    data_sources: list[str] = Field(default_factory=list)


@dataclass
class AgentResult:
    """Internal result from the SQL agent orchestration layer."""

    reply: str
    used_database: bool = False
    data_sources: list[str] = field(default_factory=list)
    iterations: int = 0
