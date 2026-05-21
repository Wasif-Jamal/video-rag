from llama_index.core.schema import (
    ImageNode,
    TextNode,
)
from llama_index.vector_stores.qdrant import (
    QdrantVectorStore,
)
from llama_index.core import (
    StorageContext,
    Settings,
)
from llama_index.core.indices.multi_modal import (
    MultiModalVectorStoreIndex,
)

from app.services.clip_embedding import (
    CLIPEmbedding,
)
from app.services.qdrant_service import (
    qdrant_service,
)
from app.config.qdrant_config import qdrant_config
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)

# Initialize our custom CLIPEmbedding model as the default embed model in Settings
Settings.embed_model = CLIPEmbedding()


class IndexingService:

    def index_nodes(
        self,
        text_nodes: list[TextNode],
        image_nodes: list[ImageNode],
    ):

        logger.info(
            "Starting native multimodal indexing via LlamaIndex"
        )

        # 1. Initialize text QdrantVectorStore
        text_store = QdrantVectorStore(
            client=qdrant_service.client,
            collection_name=(
                qdrant_config
                .get_collection_name()
            ),
        )

        # 2. Initialize image QdrantVectorStore
        image_store = QdrantVectorStore(
            client=qdrant_service.client,
            collection_name=(
                f"{qdrant_config.get_collection_name()}_image"
            ),
        )

        # 3. Initialize StorageContext with text_store and add image_store
        storage_context = (
            StorageContext
            .from_defaults(
                vector_store=text_store
            )
        )
        storage_context.add_vector_store(
            vector_store=image_store,
            namespace="image",
        )

        # 4. Create MultiModalVectorStoreIndex from both text and image nodes
        MultiModalVectorStoreIndex(
            nodes=text_nodes + image_nodes,
            storage_context=storage_context,
            image_vector_store=image_store,
            image_embed_model=Settings.embed_model,
        )

        logger.info(
            "Native multimodal indexing complete"
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