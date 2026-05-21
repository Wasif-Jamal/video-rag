from llama_index.core import (
    Settings,
)
from llama_index.core.indices.multi_modal import (
    MultiModalVectorStoreIndex,
)
from llama_index.vector_stores.qdrant import (
    QdrantVectorStore,
)

from app.config.qdrant_config import qdrant_config
from app.services.clip_embedding import (
    CLIPEmbedding,
)
from app.services.qdrant_service import (
    qdrant_service,
)
from app.config.log_config import (
    LogConfig,
)

logger = LogConfig.get_logger(__name__)

# Initialize our custom CLIPEmbedding model as the default embed model in Settings
Settings.embed_model = CLIPEmbedding()


class RetrievalService:

    def __init__(self):

        self.index = None

    def initialize(self):

        logger.info(
            "Initializing native multimodal retrieval service"
        )

        text_store = (
            QdrantVectorStore(
                client=(
                    qdrant_service.client
                ),
                collection_name=(
                    qdrant_config.get_collection_name()
                ),
            )
        )

        image_store = (
            QdrantVectorStore(
                client=(
                    qdrant_service.client
                ),
                collection_name=(
                    f"{qdrant_config.get_collection_name()}_image"
                ),
            )
        )

        self.index = (
            MultiModalVectorStoreIndex
            .from_vector_store(
                vector_store=text_store,
                image_vector_store=image_store,
                image_embed_model=Settings.embed_model,
            )
        )

        logger.info(
            "Native multimodal retrieval service initialized"
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        retriever = (
            self.index
            .as_retriever(
                similarity_top_k=top_k,
                image_similarity_top_k=top_k,
            )
        )

        nodes = retriever.retrieve(
            query
        )

        logger.info(
            f"Retrieved "
            f"{len(nodes)} multimodal nodes"
        )

        return nodes


retrieval_service = (
    RetrievalService()
)