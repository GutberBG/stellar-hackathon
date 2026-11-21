"""Domain exceptions and FastAPI custom exception handlers."""
from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AyniException(Exception):
    """Base domain exception for Ayni Cacao."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class EntityNotFoundException(AyniException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with ID '{entity_id}' not found.",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"entity": entity_name, "id": str(entity_id)},
        )


class InsufficientLiquidityException(AyniException):
    def __init__(self, requested: float, available: float):
        super().__init__(
            message=f"Liquidity pool has insufficient funds. Requested: ${requested:,.2f} USDC, Available: ${available:,.2f} USDC.",
            code="INSUFFICIENT_LIQUIDITY",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"requested_usdc": requested, "available_usdc": available},
        )


class InvalidOperationException(AyniException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="INVALID_OPERATION",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class FactoringValidationException(AyniException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="FACTORING_VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


async def ayni_exception_handler(request: Request, exc: AyniException) -> JSONResponse:
    """Format domain exceptions into a uniform JSON response structure."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )
