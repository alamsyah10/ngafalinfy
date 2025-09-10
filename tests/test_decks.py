from fastapi import status
from fastapi.testclient import TestClient


def test_create_deck_success(client: TestClient):
    payload = {"name": "JLPT N4", "description": "deck buat jlpt n4"}
    resp = client.post("/decks", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED, resp.text
    body = resp.json()
    assert body["id"] == 1001
    assert body["name"] == "JLPT N4"
    assert body["ownerId"] == 42
    assert body["description"] == "deck buat jlpt n4"


def test_create_deck_validation_error(client: TestClient):
    # Missing required 'name' -> FastAPI returns 422
    resp = client.post("/decks", json={"description": "no name"})
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_deck_success(client: TestClient):
    payload = {"name": "Updated Deck", "description": "Updated desc"}
    resp = client.put("/decks/10", json=payload)
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert body["id"] == 10
    assert body["name"] == "Updated Deck"
    assert body["ownerId"] == 42
    assert body["description"] == "Updated desc"


def test_update_deck_not_found(client: TestClient):
    payload = {"name": "New Name"}
    resp = client.put("/decks/404", json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text
    body = resp.json()
    assert body["code"] == "not_found"


def test_delete_deck_success(client: TestClient):
    resp = client.delete("/decks/10")
    # Router is configured for 202 ACCEPTED
    assert resp.status_code == status.HTTP_202_ACCEPTED, resp.text


def test_delete_deck_not_found(client: TestClient):
    resp = client.delete("/decks/404")
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_list_decks_success(client: TestClient):
    resp = client.get("/decks")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    # fastapi-pagination Page schema keys
    assert "items" in body and isinstance(body["items"], list)
    assert body["total"] == 2
    assert body["page"] == 1
    assert body["size"] == 50
    assert body["pages"] == 1
    assert len(body["items"]) == 2
    assert body["items"][0]["ownerId"] == 42


def test_path_validation_deck_id_must_be_int(client: TestClient):
    resp = client.put("/decks/abc", json={"name": "X"})
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
