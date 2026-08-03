import pytest
from fastapi.testclient import TestClient


class TestGetMyProfile:
    def test_returns_profile_for_current_user(self, client: TestClient):
        res = client.get("/me/profile")

        assert res.status_code == 200
        data = res.json()
        assert data["userId"] == 42

    def test_returns_profile_fields(self, client: TestClient):
        res = client.get("/me/profile")

        data = res.json()
        assert "bio" in data
        assert "avatarUrl" in data
        assert "phone" in data
        assert "location" in data
        assert "website" in data

    def test_requires_auth(self, app, client: TestClient):
        from src.api.composition.auth import get_current_user_id_usecase
        from fastapi import HTTPException

        app.dependency_overrides[get_current_user_id_usecase] = lambda: (_ for _ in ()).throw(
            HTTPException(status_code=401, detail="Unauthorized")
        )
        res = client.get("/me/profile")
        assert res.status_code == 401
        # restore
        app.dependency_overrides[get_current_user_id_usecase] = lambda: 42


class TestUpdateMyProfile:
    def test_update_bio(self, client: TestClient):
        res = client.patch("/me/profile", json={"bio": "Hello world"})

        assert res.status_code == 200
        assert res.json()["bio"] == "Hello world"

    def test_update_partial_fields(self, client: TestClient):
        res = client.patch(
            "/me/profile",
            json={"location": "Jakarta", "website": "https://example.com"},
        )

        assert res.status_code == 200
        data = res.json()
        assert data["location"] == "Jakarta"
        assert data["website"] == "https://example.com"

    def test_update_with_empty_body_succeeds(self, client: TestClient):
        res = client.patch("/me/profile", json={})

        assert res.status_code == 200

    def test_bio_too_long_returns_422(self, client: TestClient):
        res = client.patch("/me/profile", json={"bio": "x" * 501})

        assert res.status_code == 422

    def test_phone_too_long_returns_422(self, client: TestClient):
        res = client.patch("/me/profile", json={"phone": "0" * 21})

        assert res.status_code == 422

    def test_response_has_user_id(self, client: TestClient):
        res = client.patch("/me/profile", json={"bio": "test"})

        assert res.status_code == 200
        assert res.json()["userId"] == 42
