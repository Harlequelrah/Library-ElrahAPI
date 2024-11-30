from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except SQLAlchemyError as db_error:
            return JSONResponse(
                status_code=500,
                content={"error": "Database error", "details": str(db_error)},
            )
        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code, content={"detail": http_exc.detail}
            )
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred", "details": str(exc)},
            )
