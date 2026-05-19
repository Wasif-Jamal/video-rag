import requests

from config.app_config import (
    config,
)


class APIClient:

    def ingest_video(
        self,
        url: str,
    ):

        response = requests.post(
            (
                f"{config.BACKEND_URL}"
                "/video/youtube"
            ),
            json={
                "url": url,
            },
        )

        response.raise_for_status()

        return response.json()

    def chat(
        self,
        query: str,
    ):

        response = requests.post(
            (
                f"{config.BACKEND_URL}"
                "/chat"
            ),
            json={
                "query": query,
            },
        )

        response.raise_for_status()

        return response.json()


api_client = APIClient()