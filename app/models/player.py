from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PlayerBase(BaseModel):
	name: str


class PlayerCreate(PlayerBase):
	pass


class PlayerRead(PlayerBase):
	id: UUID
	created_at: datetime


class Player(PlayerBase):
	id: UUID = Field(default_factory=uuid4)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
