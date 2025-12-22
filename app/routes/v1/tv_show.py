

from typing import List
from fastapi import APIRouter, Path, Query

from app.schemas.responses.tv_show_response import TVShowResponse
from app.services.external.tvmaze_client import tv_client


router = APIRouter(prefix="/api/v1", tags=["Tv Shows"])

@router.get("/search", 
            response_model=List[TVShowResponse],
            summary="Search for TV series",
            description="Search for TV shows by title using the global database.")
async def search_tv_series(q: str = Query(..., example="Breaking Bad")):
    return await tv_client.search_shows(q)

@router.get("/{show_id}",
            response_model=TVShowResponse,
            summary="Get TV show details",
            description="Retrieve comprehensive information about a specific TV series using its unique ID.")
async def get_show_info(show_id: int = Path(..., example=169)):
    return await tv_client.get_show_details(show_id)