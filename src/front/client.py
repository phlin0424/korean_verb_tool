from front.config import settings

from fastapi import HTTPException
import httpx


class KoreanVerbNegativeClient:
    def __init__(self):
        self.api_server_url = settings.api_server_url
        self.client = httpx.AsyncClient()

    def get_random_verb(self) -> dict:
        """Requesting the api endpoint: /negative_forms_random.

        Raises:
            HTTPException: _description_

        Returns:
            dict: _description_
        """
        api_url = f"{self.api_server_url}/negative_forms_random"
        try:
            response = httpx.get(api_url)

            return response.json()

        except Exception as e:
            error_msg = f"Error during requesting{api_url}."
            raise HTTPException(status_code=500, detail=error_msg) from e
