from src.domain.model.common import CustomBaseModel


class HealthCheckResponse(CustomBaseModel):
    name: str
    version: str


class TestAccessResponse(CustomBaseModel):
    ok: bool
    user_id: int


class MeResponse(CustomBaseModel):
    id: int
    email: str
    display_name: str | None = None
    picture_url: str | None = None
    provider: str | None = None
