from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Player(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	name: str
	created_at: datetime = Field(default_factory=datetime.now)
