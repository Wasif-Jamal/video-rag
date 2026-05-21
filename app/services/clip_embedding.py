from typing import Any
from llama_index.embeddings.clip import (
    ClipEmbedding,
)


class CLIPEmbedding(ClipEmbedding):
    """LlamaIndex-native CLIP embedding class."""

    def __init__(self, **kwargs: Any):
        super().__init__(
            model_name="ViT-B/32",
            **kwargs,
        )
