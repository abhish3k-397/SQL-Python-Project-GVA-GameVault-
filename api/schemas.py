"""Pydantic request/response models."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    country: str = "India"


class UserResponse(BaseModel):
    userId: int
    username: str
    email: str
    role: str
    walletBalance: float
    country: str | None = None


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


class PurchaseRequest(BaseModel):
    paymentMethod: str = Field(
        ...,
        description="Wallet, Credit Card, Debit Card, UPI, or PayPal",
    )


class ReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = ""


class AddGameRequest(BaseModel):
    title: str
    developerName: str
    publisherName: str
    price: float
    releaseDate: str


class ApplyDiscountRequest(BaseModel):
    discountPercent: float = Field(..., gt=0, le=100)
    startDate: str
    endDate: str


class MessageResponse(BaseModel):
    message: str
