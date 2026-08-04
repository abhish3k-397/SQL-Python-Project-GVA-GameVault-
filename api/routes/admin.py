"""Admin routes: games, discounts, analytics, users."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.auth import require_admin
from api.schemas import AddGameRequest, ApplyDiscountRequest, MessageResponse, UserResponse
from api.utils import serialize_rows
from services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/games", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_game(body: AddGameRequest, _: Annotated[UserResponse, require_admin]):
    success = AdminService.add_game(
        body.title,
        body.developerName,
        body.publisherName,
        body.price,
        body.releaseDate,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add game",
        )
    return MessageResponse(message=f"Game '{body.title}' added successfully")


@router.post("/games/{game_id}/discount", response_model=MessageResponse)
def apply_discount(
    game_id: int,
    body: ApplyDiscountRequest,
    _: Annotated[UserResponse, require_admin],
):
    success = AdminService.apply_discount(
        game_id,
        body.discountPercent,
        body.startDate,
        body.endDate,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to apply discount",
        )
    return MessageResponse(
        message=f"{body.discountPercent}% discount applied to game {game_id}"
    )


@router.get("/analytics/top-selling")
def get_top_selling(_: Annotated[UserResponse, require_admin]):
    games = AdminService.get_top_selling_games()
    return serialize_rows(games)


@router.get("/analytics/revenue-by-developer")
def get_revenue_by_developer(_: Annotated[UserResponse, require_admin]):
    revenue = AdminService.get_revenue_by_developer()
    return serialize_rows(revenue)


@router.get("/analytics/total-revenue")
def get_total_revenue(_: Annotated[UserResponse, require_admin]):
    total = AdminService.get_total_store_revenue()
    return {"totalRevenue": total}


@router.get("/users")
def get_users(_: Annotated[UserResponse, require_admin]):
    users = AdminService.get_registered_users()
    return serialize_rows(users)
