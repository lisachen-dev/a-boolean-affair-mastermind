from uuid import UUID

from fastapi import APIRouter

from app.app_context import player_service
from app.models.player import PlayerCreate, PlayerRead

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", response_model=PlayerRead)
def create_player(new_player: PlayerCreate):
	player = player_service.create(new_player.name)

	return player_service.to_player_read(player)


@router.get("/{player_id}", response_model=PlayerRead)
def get_player(player_id: UUID):
	player = player_service.get(player_id=player_id)
	return player_service.to_player_read(player)


@router.get("/", response_model=list[PlayerRead])
def get_all_players():
	return player_service.get_all()
