from fastapi import status
from fastapi.testclient import TestClient


def test_create_card_success(client: TestClient):
    payload = {"front": "水", "back": "water", "notes": "common kanji"}
    resp = client.post("/decks/10/cards", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED, resp.text
    body = resp.json()
    assert body["deckId"] == 10
    assert body["front"] == "水"
    assert body["back"] == "water"
    assert "id" in body
    assert body["isActive"] is True


def test_list_cards_success(client: TestClient):
    # Uses default pagination params page=1, size=50 via Depends(Params)
    resp = client.get("/decks/10/cards")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert "items" in body and isinstance(body["items"], list)
    assert "total" in body and body["total"] >= 1
    assert body["items"][0]["deckId"] == 10


def test_get_card_success(client: TestClient):
    resp = client.get("/decks/10/cards/123")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert body["id"] == 123
    assert body["deckId"] == 10


def test_update_card_success(client: TestClient):
    payload = {"front": "木", "back": "tree", "notes": "kanji N5", "is_active": True}
    resp = client.put("/decks/10/cards/123", json=payload)
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert body["id"] == 123
    assert body["deckId"] == 10
    assert body["front"] == "木"
    assert body["back"] == "tree"
    assert body["isActive"] is True


def test_delete_card_success(client: TestClient):
    resp = client.delete("/decks/10/cards/123")
    assert resp.status_code == status.HTTP_202_ACCEPTED, resp.text
    assert resp.text == "Accepted"


def test_get_random_active_card_success(client: TestClient):
    resp = client.get("/decks/10/cards/random")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert body["deckId"] == 10
    assert body["isActive"] is True


def test_path_validation_deck_id_must_be_int(client: TestClient):
    resp = client.get("/decks/abc/cards/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_path_validation_card_id_must_be_int(client):
    resp = client.get("/decks/10/cards/abc")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
