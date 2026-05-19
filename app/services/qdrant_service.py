from uuid import uuid4

from qdrant_client import (
    QdrantClient,
)
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.config.qdrant_config import (
    qdrant_config,
)
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)


class QdrantService:

    def __init__(self):

        self.client = None

    def initialize(self):

        logger.info(
            "Initializing Qdrant client..."
        )

        self.client = (
            QdrantClient(
                url=(
                    qdrant_config
                    .get_url()
                ),
            )
        )

        self._create_collection()

        logger.info(
            "Qdrant initialized"
        )

    def _create_collection(
        self,
        vector_size: int = 512,
    ):

        collections = (
            self.client
            .get_collections()
        )

        existing = [
            collection.name
            for collection
            in collections.collections
        ]

        collection_name = (
            qdrant_config
            .get_collection_name()
        )

        if (
            collection_name
            in existing
        ):

            logger.info(
                "Qdrant collection "
                "already exists"
            )

            return

        logger.info(
            "Creating Qdrant collection"
        )

        self.client.create_collection(
            collection_name=(
                collection_name
            ),
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_point(
        self,
        embedding: list[float],
        payload: dict,
    ):

        self.client.upsert(
            collection_name=(
                qdrant_config
                .get_collection_name()
            ),
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            ],
        )


qdrant_service = (
    QdrantService()
)