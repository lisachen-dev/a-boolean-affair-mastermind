from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PlayerBase(BaseModel):
	name: str

class PlayerCreate(BaseModel):
	pass	# no extra fields for creation right now

class Player(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	name: str
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
