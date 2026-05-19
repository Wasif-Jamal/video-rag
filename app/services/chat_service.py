from app.config.log_config import (
    LogConfig,
)
from app.services.retrieval_service import (
    retrieval_service,
)

logger = LogConfig.get_logger(__name__)


class ChatService:

    def chat(
        self,
        query: str,
    ):

        retrieved_nodes = (
            retrieval_service
            .retrieve(query)
        )

        context_chunks = []

        images = []

        for node in retrieved_nodes:

            metadata = (
                node.metadata
            )

            text = (
                node.text
            )

            context_chunks.append(
                text
            )

            frame_paths = (
                metadata.get(
                    "frame_paths",
                    [],
                )
            )

            for path in frame_paths:

                images.append(
                    {
                        "image_path": path,
                        "score": (
                            node.score
                        ),
                    }
                )

        answer = "\n\n".join(
            context_chunks
        )

        return {
            "answer": answer,
            "images": images,
        }


chat_service = (
    ChatService()
)