"""Game catalog routes (public + authenticated)."""

from fastapi import APIRouter, HTTPException, status

from api.utils import serialize_row, serialize_rows
from services.customer_service import CustomerService

router = APIRouter(prefix="/games", tags=["games"])


@router.get("")
def get_catalog():
    catalog = CustomerService.get_catalog()
    return serialize_rows(catalog, camel_case=False)


@router.get("/{game_id}")
def get_game_details(game_id: int):
    details = CustomerService.get_game_details(game_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )
    return serialize_row(details)
