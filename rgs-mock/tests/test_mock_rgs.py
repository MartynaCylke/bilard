from fastapi.testclient import TestClient

from mock_rgs import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_wallet_balance_changes_after_play():
    session_id = "test-session"
    auth_response = client.post("/wallet/authenticate", json={"sessionID": session_id})
    starting_balance = auth_response.json()["balance"]["amount"]

    play_response = client.post(
        "/wallet/play",
        json={"sessionID": session_id, "amount": 250, "mode": "BASE"},
    )

    assert play_response.status_code == 200
    assert play_response.json()["balance"]["amount"] == starting_balance - 250
    assert play_response.json()["round"]["state"][0]["type"] == "setBoard"


def test_play_rejects_non_positive_amount():
    response = client.post(
        "/wallet/play",
        json={"sessionID": "invalid-bet", "amount": 0, "mode": "BASE"},
    )

    assert response.status_code == 422
