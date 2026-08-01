from fastapi import status
from fastapi.testclient import TestClient


def test_get_next_due_card_success(client: TestClient):
    """Test getting next due card in a deck"""
    resp = client.get("/decks/10/study/next")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert "card" in body
    assert body["card"]["deckId"] == 10
    assert body["card"]["isActive"] is True


def test_get_next_due_card_no_cards(client: TestClient):
    """Test when no cards are due in the deck"""
    resp = client.get("/decks/999/study/next")
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_get_next_due_card_deck_not_found(client: TestClient):
    """Test when deck doesn't exist"""
    resp = client.get("/decks/404/study/next")
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_answer_card_success(client: TestClient):
    """Test answering a card successfully"""
    payload = {"ease_given": 4}
    resp = client.post("/decks/10/study/123/answer", json=payload)
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert "card" in body and "log" in body
    assert body["card"]["id"] == 123
    assert body["card"]["deckId"] == 10
    assert body["log"]["easeGiven"] == 4
    assert body["log"]["cardId"] == 123


def test_answer_card_ease_too_low(client: TestClient):
    """Test answer with ease_given < 0 (validation error)"""
    payload = {"ease_given": -1}
    resp = client.post("/decks/10/study/123/answer", json=payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, resp.text


def test_answer_card_ease_too_high(client: TestClient):
    """Test answer with ease_given > 5 (validation error)"""
    payload = {"ease_given": 6}
    resp = client.post("/decks/10/study/123/answer", json=payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, resp.text


def test_answer_card_missing_ease_given(client: TestClient):
    """Test answer without ease_given field"""
    payload = {}
    resp = client.post("/decks/10/study/123/answer", json=payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, resp.text


def test_answer_card_deck_not_found(client: TestClient):
    """Test answering card in non-existent deck"""
    payload = {"ease_given": 4}
    resp = client.post("/decks/404/study/123/answer", json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_path_validation_deck_id_must_be_int(client: TestClient):
    """Test path validation for deck_id"""
    resp = client.get("/decks/abc/study/next")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_path_validation_card_id_must_be_int(client: TestClient):
    """Test path validation for card_id"""
    payload = {"ease_given": 4}
    resp = client.post("/decks/10/study/abc/answer", json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
