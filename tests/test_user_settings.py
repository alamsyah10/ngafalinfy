from fastapi.testclient import TestClient


class TestGetMySettings:
    def test_returns_settings_for_current_user(self, client: TestClient):
        res = client.get("/me/settings")

        assert res.status_code == 200
        assert res.json()["userId"] == 42

    def test_returns_all_settings_fields(self, client: TestClient):
        res = client.get("/me/settings")

        data = res.json()
        assert "language" in data
        assert "timezone" in data
        assert "theme" in data
        assert "dailyReviewGoal" in data
        assert "notificationsEnabled" in data

    def test_default_values(self, client: TestClient):
        res = client.get("/me/settings")

        data = res.json()
        assert data["language"] == "en"
        assert data["timezone"] == "UTC"
        assert data["theme"] == "system"
        assert data["dailyReviewGoal"] == 20
        assert data["notificationsEnabled"] is True


class TestUpdateMySettings:
    def test_update_language(self, client: TestClient):
        res = client.patch("/me/settings", json={"language": "id"})

        assert res.status_code == 200
        assert res.json()["language"] == "id"

    def test_update_timezone(self, client: TestClient):
        res = client.patch("/me/settings", json={"timezone": "Asia/Jakarta"})

        assert res.status_code == 200
        assert res.json()["timezone"] == "Asia/Jakarta"

    def test_update_theme(self, client: TestClient):
        res = client.patch("/me/settings", json={"theme": "dark"})

        assert res.status_code == 200
        assert res.json()["theme"] == "dark"

    def test_update_daily_review_goal(self, client: TestClient):
        res = client.patch("/me/settings", json={"dailyReviewGoal": 50})

        assert res.status_code == 200
        assert res.json()["dailyReviewGoal"] == 50

    def test_update_notifications(self, client: TestClient):
        res = client.patch("/me/settings", json={"notificationsEnabled": False})

        assert res.status_code == 200
        assert res.json()["notificationsEnabled"] is False

    def test_empty_body_succeeds(self, client: TestClient):
        res = client.patch("/me/settings", json={})

        assert res.status_code == 200

    def test_invalid_timezone_returns_422(self, client: TestClient):
        res = client.patch("/me/settings", json={"timezone": "Moon/Crater"})

        assert res.status_code == 422

    def test_invalid_language_returns_422(self, client: TestClient):
        res = client.patch("/me/settings", json={"language": "xx"})

        assert res.status_code == 422

    def test_daily_review_goal_zero_returns_422(self, client: TestClient):
        res = client.patch("/me/settings", json={"dailyReviewGoal": 0})

        assert res.status_code == 422

    def test_daily_review_goal_over_limit_returns_422(self, client: TestClient):
        res = client.patch("/me/settings", json={"dailyReviewGoal": 501})

        assert res.status_code == 422
