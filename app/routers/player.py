from uuid import UUID

from fastapi import APIRouter

from app.models.player import PlayerCreate

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", response_model=PlayerRead)
def create_player(new_player: PlayerCreate):
	pass


@router.get("/{player_id}")
def get_player(player_id: UUID):
	pass


@router.get("/")
def get_all_players():
	pass
