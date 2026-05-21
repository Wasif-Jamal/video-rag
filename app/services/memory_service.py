from collections import defaultdict

from app.config.log_config import (
    LogConfig,
)

logger = LogConfig.get_logger(__name__)


class MemoryService:
    """
    In-memory short-term conversation memory.
    """

    def __init__(self):

        self.memory = defaultdict(
            list
        )

    def get_history(
        self,
        session_id: str,
    ) -> list[dict]:

        return self.memory[
            session_id
        ]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        self.memory[
            session_id
        ].append(
            {
                "role": role,
                "content": content,
            }
        )

        logger.info(
            f"Added {role} message "
            f"to session {session_id}"
        )

    def clear_history(
        self,
        session_id: str,
    ):

        if (
            session_id
            in self.memory
        ):

            del self.memory[
                session_id
            ]

            logger.info(
                f"Cleared memory for "
                f"session {session_id}"
            )

    def build_conversation_context(
        self,
        session_id: str,
    ) -> str:

        history = (
            self.get_history(
                session_id
            )
        )

        if not history:

            return ""

        conversation = []

        for message in history:

            role = (
                message["role"]
                .capitalize()
            )

            content = (
                message["content"]
            )

            conversation.append(
                f"{role}: {content}"
            )

        return "\n".join(
            conversation
        )


memory_service = (
    MemoryService()
)