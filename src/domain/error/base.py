class ApplicationError(Exception):
    status: int
    code: str
    message: str

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.code = self.__class__.__name__
        self.message = message

    def __str__(self) -> str:
        return f"[{self.code}]: {self.message}"


class InternalServerError(ApplicationError):
    status = 500

    def __init__(self, message: str):
        super().__init__(self.status, message)


class UnauthorizedError(ApplicationError):
    status = 401

    def __init__(self, message):
        super().__init__(status=self.status, message=message)


class UserNotFoundError(ApplicationError):
    status = 404

    def __init__(self, message):
        super().__init__(status=self.status, message=message)


class ResourceConflictError(ApplicationError):
    status = 409

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(status=self.status, message=message)


class OAuthClientNotConfiguredError(ApplicationError):
    status = 500

    def __init__(self, message: str = "OAuth client 'google' not configured"):
        super().__init__(status=self.status, message=message)


class OAuthInvalidUserInfoError(ApplicationError):
    status = 400

    def __init__(self, message: str = "Invalid user info"):
        super().__init__(status=self.status, message=message)


class OAuthAuthenticationFailedError(ApplicationError):
    status = 500

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(status=self.status, message=message)
