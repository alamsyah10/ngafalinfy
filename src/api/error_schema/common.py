from pydantic import BaseModel, Field


class ErrorMessageValidationError(BaseModel):
    status: str = Field(examples=["400"], description="HTTP status code")
    code: str = Field(examples=["validation_error"], description="Error code")
    message: str = Field(
        examples=["id[xxx] is invalid uuid"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "Validation Error"


class ErrorMessageResourceInProgressError(BaseModel):
    status: str = Field(examples=["202"], description="HTTP status code")
    code: str = Field(examples=["resource_in_progress_error"], description="Error code")
    message: str = Field(
        examples=["resource[xxx] is still in progress"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "Resource In Progress Error"


class ErrorMessageResourceNotFoundError(BaseModel):
    status: str = Field(examples=["404"], description="HTTP status code")
    code: str = Field(examples=["resource_not_found_error"], description="Error code")
    message: str = Field(
        examples=["resource[xxx] is not found"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "Resource Not Found Error"


class ErrorMessageResourceConflictError(BaseModel):
    status: str = Field(examples=["409"], description="HTTP status code")
    code: str = Field(examples=["resource_conflict_error"], description="Error code")
    message: str = Field(
        examples=["resource[xxx] already exists"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "Resource Conflict Error"


class ErrorMessageInternalServerError(BaseModel):
    status: str = Field(examples=["500"], description="HTTP status code")
    code: str = Field(examples=["internal_server_error"], description="Error code")
    message: str = Field(examples=["runtime error"], description="Error message")

    class Config:
        populate_by_name = True
        title = "Internal Server Error"


class ErrorMessageAuthorizationError(BaseModel):
    status: str = Field(examples=["401"], description="HTTP status code")
    code: str = Field(examples=["authorization_error"], description="Error code")
    message: str = Field(
        examples=["Not authorized to access this resource"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "Authorization Error"


class ErrorMessageUserNotFoundError(BaseModel):
    status: str = Field(examples=["404"], description="HTTP status code")
    code: str = Field(examples=["user_not_found_error"], description="Error code")
    message: str = Field(
        examples=["User with id=xxx not found"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "User Not Found Error"


class ErrorMessageOAuthClientNotConfigured(BaseModel):
    status: str = Field(examples=["500"], description="HTTP status code")
    code: str = Field(
        examples=["oauth_client_not_configured"], description="Error code"
    )
    message: str = Field(
        examples=["OAuth client 'google' not configured"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "OAuth Client Not Configured Error"


class ErrorMessageOAuthInvalidUserInfo(BaseModel):
    status: str = Field(examples=["400"], description="HTTP status code")
    code: str = Field(examples=["oauth_invalid_userinfo"], description="Error code")
    message: str = Field(
        examples=["Google userinfo response missing email"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "OAuth Invalid User Info Error"


class ErrorMessageOAuthAccountConflict(BaseModel):
    status: str = Field(examples=["409"], description="HTTP status code")
    code: str = Field(examples=["oauth_account_conflict"], description="Error code")
    message: str = Field(
        examples=["Account already exists with this email"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "OAuth Account Conflict Error"


class ErrorMessageOAuthAuthenticationFailed(BaseModel):
    status: str = Field(examples=["500"], description="HTTP status code")
    code: str = Field(
        examples=["oauth_authentication_failed"], description="Error code"
    )
    message: str = Field(
        examples=["Google authentication failed"], description="Error message"
    )

    class Config:
        populate_by_name = True
        title = "OAuth Authentication Failed Error"
