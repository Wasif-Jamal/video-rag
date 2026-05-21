from qdrant_client import (
    QdrantClient,
)
from qdrant_client.models import (
    Distance,
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

        # Check for both main collection and image collection
        for col_name in [collection_name, f"{collection_name}_image"]:
            if col_name in existing:
                logger.info(
                    f"Qdrant collection {col_name} already exists"
                )
                continue

            logger.info(
                f"Creating Qdrant collection: {col_name}"
            )

            self.client.create_collection(
                collection_name=col_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )


qdrant_service = (
    QdrantService()
)