from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Player(BaseModel):
	model_config = ConfigDict(extra="forbid")

	id: UUID = Field(default_factory=uuid4)
	name: str
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
