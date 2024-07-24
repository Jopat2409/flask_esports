

def test_get_player(client):
    response = client.get("/tf2/player/76561197970669109").json
    assert response["success"]
    player_data = response["data"]
    assert player_data.get("alias", None) == "b4nny"
    assert player_data.get("current-team", None) == 12737
