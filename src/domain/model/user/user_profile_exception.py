from src.domain.error.base import ResourceNotFoundError


class UserProfileNotFoundError(ResourceNotFoundError):
    def __init__(self, user_id: int):
        super().__init__(message=f"profile for user[{user_id}] is not found")


class UserSettingsNotFoundError(ResourceNotFoundError):
    def __init__(self, user_id: int):
        super().__init__(message=f"settings for user[{user_id}] is not found")
