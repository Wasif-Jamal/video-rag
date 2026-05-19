import os


class QdrantConfig:

    def __init__(self):

        self.url = os.getenv(
            "QDRANT_URL",
            "http://localhost:6333",
        )

        self.collection_name = (
            os.getenv(
                "QDRANT_COLLECTION",
                "video_rag_multimodal",
            )
        )

    def get_url(self) -> str:

        return self.url

    def get_collection_name(
        self,
    ) -> str:

        return (
            self.collection_name
        )


qdrant_config = (
    QdrantConfig()
)