"""JWT authentication utilities and FastAPI dependencies."""

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.schemas import UserResponse

JWT_SECRET = os.getenv("JWT_SECRET", "gamevault-dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

security = HTTPBearer(auto_error=False)


def create_token(user_id: int, username: str, email: str, role: str, wallet_balance: float) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "email": email,
        "role": role,
        "walletBalance": wallet_balance,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> UserResponse:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    payload = decode_token(credentials.credentials)
    return UserResponse(
        userId=int(payload["sub"]),
        username=payload["username"],
        email=payload["email"],
        role=payload["role"],
        walletBalance=float(payload.get("walletBalance", 0)),
    )


def require_customer(user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    if user.role != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer access required")
    return user


def require_admin(user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
