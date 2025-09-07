from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from src.api.log.logger import get_logger, init_logger
from src.api.middleware.error_handling_middleware import ErrorHandlingMiddleware
from src.api.middleware.router_logging_middleware import RouterLoggingMiddleware
from src.api.router import auth_google, checkhealth
from src.config import settings

init_logger()
logger = get_logger("backend")

app = FastAPI(title=settings.API_NAME, debug=settings.DEBUG, version=settings.VERSION)


@app.exception_handler(RequestValidationError)
async def custom_request_validation_error_handler(
    request: Request, exception: RequestValidationError
):
    """Process to format validation errors in the same way as other error responses"""
    logger.error(exception.errors())
    return JSONResponse(
        {
            "status": status.HTTP_400_BAD_REQUEST,
            "code": "request_schema_validation_error",
            "message": exception.errors().__str__(),
        },
        status.HTTP_400_BAD_REQUEST,
    )


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_allow_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session (required by Authlib to store OAuth state)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    same_site=settings.SESSION_SAMESITE,  # "lax" or "none"
    https_only=settings.SESSION_HTTPS_ONLY,
)
app.add_middleware(ErrorHandlingMiddleware, logger=logger)
app.add_middleware(RouterLoggingMiddleware, logger=logger)

# Routers
app.include_router(auth_google.router)
app.include_router(checkhealth.router)
