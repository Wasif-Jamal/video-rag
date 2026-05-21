from app.config.log_config import (
    LogConfig,
)
from app.prompts.prompts import (
    prompt_manager,
)
from app.services.llm_service import (
    llm_service,
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
            retrieval_service.retrieve(
                query
            )
        )

        context_chunks = []
        images = []
        seen_paths = set()

        for node in retrieved_nodes:
            actual_node = getattr(node, "node", node)

            node_text = (
                getattr(actual_node, "text", "")
                or ""
            )
            if node_text:
                context_chunks.append(node_text)

            metadata = (
                getattr(
                    actual_node,
                    "metadata",
                    {},
                )
                or {}
            )

            # Extract from TextNode's metadata frame_paths
            frame_paths = metadata.get(
                "frame_paths", []
            )
            for path in frame_paths:
                if path not in seen_paths:
                    seen_paths.add(path)
                    images.append(
                        {
                            "image_path": path,
                            "score": node.score,
                        }
                    )

            # Extract from ImageNode's direct image_path
            image_path = getattr(
                actual_node, "image_path", None
            )
            if (
                image_path
                and image_path not in seen_paths
            ):
                seen_paths.add(image_path)
                images.append(
                    {
                        "image_path": image_path,
                        "score": node.score,
                    }
                )

        context = "\n\n".join(
            context_chunks
        )

        prompt = (
            prompt_manager
            .get_chat_prompt(
                question=query,
                context=context,
            )
        )

        llm = (
            llm_service.get_llm()
        )

        response = llm.invoke(
            prompt
        )

        logger.info(
            "Generated RAG response"
        )

        answer = ""

        if isinstance(
            response.content,
            str,
        ):

            answer = response.content

        elif isinstance(
            response.content,
            list,
        ):

            text_parts = []

            for item in response.content:

                if (
                    isinstance(item, dict)
                    and item.get("type") == "text"
                ):

                    text_parts.append(
                        item.get("text", "")
                    )

            answer = "\n".join(
                text_parts
            )

        return {
            "answer": answer,
            "images": images,
        }


chat_service = (
    ChatService()
)