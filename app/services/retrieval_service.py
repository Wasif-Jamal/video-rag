from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.vector_stores.qdrant import (
    QdrantVectorStore,
)
from llama_index.core import (
    Settings,
)
from llama_index.core.embeddings import (
    MockEmbedding,
)

from app.config.qdrant_config import qdrant_config
from app.services.qdrant_service import (
    qdrant_service,
)
from app.config.log_config import (
    LogConfig,
)

logger = LogConfig.get_logger(__name__)

Settings.embed_model = (
    MockEmbedding(
        embed_dim=512
    )
)


class RetrievalService:

    def __init__(self):

        self.index = None

    def initialize(self):

        logger.info(
            "Initializing retrieval service"
        )

        vector_store = (
            QdrantVectorStore(
                client=(
                    qdrant_service.client
                ),
                collection_name=(
                    qdrant_config.get_collection_name()
                ),
            )
        )

        self.index = (
            VectorStoreIndex
            .from_vector_store(
                vector_store
            )
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        retriever = (
            self.index
            .as_retriever(
                similarity_top_k=top_k
            )
        )

        nodes = retriever.retrieve(
            query
        )

        logger.info(
            f"Retrieved "
            f"{len(nodes)} nodes"
        )

        return nodes


retrieval_service = (
    RetrievalService()
)