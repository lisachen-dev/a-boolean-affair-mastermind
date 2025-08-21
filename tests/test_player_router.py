from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_player_path():
	response = client.post("/players?name=Lisa")
	print(response.json())
	assert response.status_code == 200
