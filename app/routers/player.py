import logging
from uuid import UUID

from fastapi import APIRouter

from app.app_context import player_service
from app.models.player import Player

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=Player)
def create_player(name: str) -> Player:
	return player_service.create(name)


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: UUID):
	return player_service.get(player_id=player_id)


@router.get("/", response_model=list[Player])
def get_all_players():
	return player_service.get_all()
