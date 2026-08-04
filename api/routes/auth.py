"""Authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.auth import create_token, get_current_user
from api.schemas import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from models.user import Admin, Customer
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest):
    user = AuthService.login(body.username, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if isinstance(user, Admin):
        role = "admin"
    elif isinstance(user, Customer):
        role = "customer"
    else:
        role = "customer"

    user_response = UserResponse(
        userId=user.user_id,
        username=user.username,
        email=user.email,
        role=role,
        walletBalance=user.wallet_balance,
        country=user.country,
    )
    token = create_token(
        user.user_id,
        user.username,
        user.email,
        role,
        user.wallet_balance,
    )
    return AuthResponse(token=token, user=user_response)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    success = AuthService.register_customer(
        body.username, body.email, body.password, body.country
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed. Username or email may already exist.",
        )

    user = AuthService.login(body.username, body.password)
    if not user or not isinstance(user, Customer):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration succeeded but login failed",
        )

    user_response = UserResponse(
        userId=user.user_id,
        username=user.username,
        email=user.email,
        role="customer",
        walletBalance=user.wallet_balance,
        country=user.country,
    )
    token = create_token(
        user.user_id,
        user.username,
        user.email,
        "customer",
        user.wallet_balance,
    )
    return AuthResponse(token=token, user=user_response)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserResponse = get_current_user):
    return current_user
