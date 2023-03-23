from typing import Any, List, Dict
from fastapi import APIRouter, status, HTTPException
from schemas.brands import Brand
from data import brands_data

# api router
router = APIRouter()


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=List[Brand],
)
async def list_brands() -> List:
    """
    Show all brands data.
    """
    return brands_data


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Brand,
)
async def get_brand(id: int) -> Dict:
    """Get a single brand"""
    brand = next((item for item in brands_data if item["id"] == id), None)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
        )
    return brand
