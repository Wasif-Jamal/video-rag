from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from app.config.env_config import (
    config,
)
from app.config.log_config import (
    LogConfig,
)

logger = LogConfig.get_logger(__name__)


class LLMService:

    def __init__(self):

        self._llm = None

    def get_llm(
        self,
    ) -> ChatGoogleGenerativeAI:

        if self._llm is None:

            api_key = (
                config
                .GOOGLE_API_KEY
            )

            if not api_key:

                raise ValueError(
                    "GOOGLE_API_KEY "
                    "not found"
                )

            logger.info(
                "Initializing Gemini "
                f"{config.GEMINI_MODEL_NAME}"
            )

            self._llm = (
                ChatGoogleGenerativeAI(
                    model=(
                        config
                        .GEMINI_MODEL_NAME
                    ),
                    google_api_key=api_key,
                    temperature=0,
                )
            )

        return self._llm


llm_service = (
    LLMService()
)