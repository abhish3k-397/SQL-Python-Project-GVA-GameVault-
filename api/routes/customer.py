"""Customer routes: library, wishlist, purchase, reviews, orders."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.auth import require_customer
from api.schemas import MessageResponse, PurchaseRequest, ReviewRequest, UserResponse
from api.utils import serialize_rows
from services.customer_service import CustomerService

router = APIRouter(tags=["customer"])


@router.post("/games/{game_id}/purchase", response_model=MessageResponse)
def purchase_game(
    game_id: int,
    body: PurchaseRequest,
    user: Annotated[UserResponse, require_customer],
):
    valid_methods = {"Wallet", "Credit Card", "Debit Card", "UPI", "PayPal"}
    if body.paymentMethod not in valid_methods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid payment method. Choose from: {', '.join(valid_methods)}",
        )

    try:
        success = CustomerService.purchase_game(user.userId, game_id, body.paymentMethod)
    except Exception as exc:
        err_msg = str(exc)
        if "already own" in err_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already own this game",
            ) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg) from exc

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Purchase failed",
        )
    return MessageResponse(message="Purchase successful. Game added to your library.")


@router.get("/library")
def get_library(user: Annotated[UserResponse, require_customer]):
    library = CustomerService.get_user_library(user.userId)
    return serialize_rows(library)


@router.get("/wishlist")
def get_wishlist(user: Annotated[UserResponse, require_customer]):
    wishlist = CustomerService.get_user_wishlist(user.userId)
    return serialize_rows(wishlist)


@router.post("/wishlist/{game_id}", response_model=MessageResponse)
def add_to_wishlist(
    game_id: int,
    user: Annotated[UserResponse, require_customer],
):
    try:
        success = CustomerService.add_to_wishlist(user.userId, game_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add to wishlist",
        )
    return MessageResponse(message="Game added to wishlist")


@router.post("/games/{game_id}/reviews", response_model=MessageResponse)
def add_review(
    game_id: int,
    body: ReviewRequest,
    user: Annotated[UserResponse, require_customer],
):
    try:
        success = CustomerService.add_review(
            user.userId, game_id, body.rating, body.comment
        )
    except Exception as exc:
        err_msg = str(exc)
        if "must own" in err_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must own this game before reviewing it",
            ) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg) from exc

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to submit review",
        )
    return MessageResponse(message="Review submitted successfully")


@router.get("/orders/history")
def get_purchase_history(user: Annotated[UserResponse, require_customer]):
    history, total_spend = CustomerService.get_purchase_history(user.userId)
    return {
        "history": serialize_rows(history),
        "totalSpend": total_spend,
    }
