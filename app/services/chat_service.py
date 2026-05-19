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

        for node in retrieved_nodes:

            context_chunks.append(
                node.text
            )

            metadata = (
                node.metadata
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