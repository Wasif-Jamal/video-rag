from app.config.log_config import (
    LogConfig,
)
from app.prompts.prompts import (
    prompt_manager,
)
from app.services.llm_service import (
    llm_service,
)
from app.services.memory_service import (
    memory_service,
)
from app.services.retrieval_service import (
    retrieval_service,
)

logger = LogConfig.get_logger(__name__)


class ChatService:
    def chat(
        self,
        session_id: str,
        query: str,
    ):

        # 1. Retrieve memory history
        history = memory_service.build_conversation_context(session_id)

        # 2. Retrieve relevant nodes
        retrieved_nodes = retrieval_service.retrieve(query)

        context_chunks = []
        images = []
        seen_paths = set()

        for node in retrieved_nodes:
            actual_node = getattr(
                node,
                "node",
                node,
            )

            node_text = (
                getattr(
                    actual_node,
                    "text",
                    "",
                )
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

            # TextNode frame paths
            frame_paths = metadata.get(
                "frame_paths",
                [],
            )

            for path in frame_paths:
                if path not in seen_paths:
                    seen_paths.add(path)

                    images.append(
                        {
                            "image_path": (path),
                            "score": (node.score),
                        }
                    )

            # ImageNode direct image
            image_path = getattr(
                actual_node,
                "image_path",
                None,
            )

            if image_path and image_path not in seen_paths:
                seen_paths.add(image_path)

                images.append(
                    {
                        "image_path": (image_path),
                        "score": (node.score),
                    }
                )

        context = "\n\n".join(context_chunks)

        # 3. Build prompt
        prompt = prompt_manager.get_chat_prompt(
            question=query,
            context=context,
            history=history,
        )

        llm = llm_service.get_llm()

        # 4. Generate response
        response = llm.invoke(prompt)

        logger.info("Generated RAG response")

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
                    isinstance(
                        item,
                        dict,
                    )
                    and item.get("type") == "text"
                ):
                    text_parts.append(
                        item.get(
                            "text",
                            "",
                        )
                    )

            answer = "\n".join(text_parts)

        # 5. Store conversation
        memory_service.add_message(
            session_id=session_id,
            role="user",
            content=query,
        )

        memory_service.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return {
            "answer": answer,
            "images": images,
        }


chat_service = ChatService()
