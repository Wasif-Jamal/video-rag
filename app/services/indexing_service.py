from llama_index.core.schema import (
    ImageNode,
    TextNode,
)

from app.services.embedding_service import (
    embedding_service,
)
from app.services.qdrant_service import (
    qdrant_service,
)
from app.config.qdrant_config import qdrant_config
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)


class IndexingService:

    def index_nodes(
        self,
        text_nodes: list[TextNode],
        image_nodes: list[ImageNode],
    ):

        logger.info(
            "Starting multimodal indexing"
        )

        # Index text nodes
        for text_node in text_nodes:

            embedding = (
                embedding_service
                .generate_text_embedding(
                    text_node.text
                )
            )

            payload = {
                "type": "text",
                "text": (
                    text_node.text
                ),
                **text_node.metadata,
            }

            qdrant_service.upsert_point(
                embedding=embedding,
                payload=payload,
            )

        # Index image nodes
        for image_node in image_nodes:

            embedding = (
                embedding_service
                .generate_image_embedding(
                    image_node.image_path
                )
            )

            payload = {
                "type": "image",
                "image_path": (
                    image_node.image_path
                ),
                **image_node.metadata,
            }

            qdrant_service.upsert_point(
                embedding=embedding,
                payload=payload,
            )

        logger.info(
            "Multimodal indexing complete"
        )

        return {
            "collection_name": (
                qdrant_config
                .get_collection_name()
            ),
            "indexed_points": (
                len(text_nodes)
                + len(image_nodes)
            ),
        }


indexing_service = (
    IndexingService()
)