from fastapi import status
from fastapi.testclient import TestClient


def test_create_review_log_success(client: TestClient):
    """Test creating a review log"""
    payload = {
        "card_id": 123,
        "ease_given": 4,
        "prev_interval": 0,
        "new_interval": 1,
        "prev_ease": 2.5,
        "new_ease": 2.6,
    }
    resp = client.post("/decks/10/review-logs", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED, resp.text
    body = resp.json()
    assert body["cardId"] == 123
    assert body["easeGiven"] == 4
    assert body["newInterval"] == 1
    assert "id" in body


def test_create_review_log_with_reviewed_at(client: TestClient):
    """Test creating a review log defaults to now when reviewed_at is omitted"""
    payload = {
        "card_id": 123,
        "ease_given": 3,
        "prev_interval": 1,
        "new_interval": 6,
        "prev_ease": 2.5,
        "new_ease": 2.4,
    }
    resp = client.post("/decks/10/review-logs", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED, resp.text
    body = resp.json()
    assert body["easeGiven"] == 3
    assert "reviewedAt" in body


def test_create_review_log_deck_not_found(client: TestClient):
    """Test creating log in non-existent deck"""
    payload = {
        "card_id": 123,
        "ease_given": 4,
        "prev_interval": 0,
        "new_interval": 1,
        "prev_ease": 2.5,
        "new_ease": 2.6,
    }
    resp = client.post("/decks/404/review-logs", json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_create_review_log_invalid_ease_given_negative(client: TestClient):
    """Test validation: ease_given must be >= 0"""
    payload = {
        "card_id": 123,
        "ease_given": -1,
        "prev_interval": 0,
        "new_interval": 1,
        "prev_ease": 2.5,
        "new_ease": 2.6,
    }
    resp = client.post("/decks/10/review-logs", json=payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, resp.text


def test_create_review_log_invalid_ease_given_too_high(client: TestClient):
    """Test validation: ease_given must be <= 5"""
    payload = {
        "card_id": 123,
        "ease_given": 6,
        "prev_interval": 0,
        "new_interval": 1,
        "prev_ease": 2.5,
        "new_ease": 2.6,
    }
    resp = client.post("/decks/10/review-logs", json=payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, resp.text


def test_list_review_logs_by_deck_success(client: TestClient):
    """Test listing review logs in a deck"""
    resp = client.get("/decks/10/review-logs")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert "items" in body and isinstance(body["items"], list)
    assert "total" in body and body["total"] >= 1
    assert body["items"][0]["cardId"] in [101, 102, 103]


def test_list_review_logs_by_deck_with_pagination(client: TestClient):
    """Test listing with pagination params"""
    resp = client.get("/decks/10/review-logs?page=1&size=10")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert "items" in body
    assert "total" in body
    assert "page" in body


def test_list_review_logs_by_deck_not_found(client: TestClient):
    """Test listing logs in non-existent deck"""
    resp = client.get("/decks/404/review-logs")
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_get_review_log_success(client: TestClient):
    """Test getting a specific review log"""
    resp = client.get("/decks/10/review-logs/1")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert body["id"] == 1
    assert body["cardId"] == 123


def test_get_review_log_not_found(client: TestClient):
    """Test getting non-existent review log"""
    resp = client.get("/decks/10/review-logs/404")
    assert resp.status_code == status.HTTP_404_NOT_FOUND, resp.text


def test_list_review_logs_by_card_success(client: TestClient):
    """Test listing review logs for a specific card"""
    resp = client.get("/decks/10/review-logs/cards/123")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert "items" in body and isinstance(body["items"], list)
    assert "total" in body
    # All items should be for card 123
    for item in body["items"]:
        assert item["cardId"] == 123


def test_list_review_logs_by_card_with_sort(client: TestClient):
    """Test listing card logs with newest_first param"""
    resp = client.get("/decks/10/review-logs/cards/123?newest_first=true")
    assert resp.status_code == status.HTTP_200_OK, resp.text
    body = resp.json()
    assert len(body["items"]) > 0


def test_path_validation_deck_id_must_be_int(client: TestClient):
    """Test path validation for deck_id"""
    resp = client.get("/decks/abc/review-logs")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_path_validation_review_log_id_must_be_int(client: TestClient):
    """Test path validation for review_log_id"""
    resp = client.get("/decks/10/review-logs/abc")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_path_validation_card_id_must_be_int(client: TestClient):
    """Test path validation for card_id in card history"""
    resp = client.get("/decks/10/review-logs/cards/abc")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
