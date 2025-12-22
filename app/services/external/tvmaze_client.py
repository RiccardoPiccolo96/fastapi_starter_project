from typing import Any, Dict, List

from app.schemas.responses.tv_show_response import TVShowResponse
from app.services.external.base_client import BaseExternalClient
from app.core.config import settings


class TVMazeClient(BaseExternalClient):
    def __init__(self):
        # API gratuita, in inglese, senza API Key
        super().__init__(base_url=settings.SERIES_TV_URL)

    async def search_shows(self, query: str) -> List[TVShowResponse]:
        """
        GET 1: Ricerca testuale di serie TV.
        """
        raw_results = await self.get(endpoint="/search/shows", params={"q": query})
        
        return [
            TVShowResponse.model_validate(item["show"]) 
            for item in raw_results
        ]

    async def get_show_details(self, show_id: int) -> TVShowResponse:
        """
        GET 2: Dettagli singoli di una serie.
        """
        raw_data = await self.get(endpoint=f"/shows/{show_id}")
        return TVShowResponse.model_validate(raw_data)

# Istanza pronta per l'uso
tv_client = TVMazeClient()