import torch
from PIL import Image
from transformers import (
    CLIPModel,
    CLIPProcessor,
)

from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)


class EmbeddingService:

    def __init__(self):

        logger.info(
            "Loading CLIP model..."
        )

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = (
            CLIPModel
            .from_pretrained(
                "openai/clip-vit-base-patch32"
            )
            .to(self.device)
        )

        self.processor = (
            CLIPProcessor
            .from_pretrained(
                "openai/clip-vit-base-patch32"
            )
        )

        logger.info(
            f"CLIP loaded on "
            f"{self.device}"
        )

    def generate_text_embedding(
        self,
        text: str,
    ) -> list[float]:

        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(self.device)

        with torch.no_grad():
            outputs = (
                self.model
                .get_text_features(
                    **inputs
                )
            )

            embedding = (
                outputs.pooler_output
                if hasattr(
                    outputs,
                    "pooler_output",
                )
                else outputs
            )

        embedding = (
            embedding
            / embedding.norm(
                p=2,
                dim=-1,
                keepdim=True,
            )
        )

        return (
            embedding[0]
            .cpu()
            .tolist()
        )

    def generate_image_embedding(
        self,
        image_path: str,
    ) -> list[float]:

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            outputs = (
                self.model
                .get_image_features(
                    **inputs
                )
            )

            embedding = (
                outputs.pooler_output
                if hasattr(
                    outputs,
                    "pooler_output",
                )
                else outputs
            )

        embedding = (
            embedding
            / embedding.norm(
                p=2,
                dim=-1,
                keepdim=True,
            )
        )

        return (
            embedding[0]
            .cpu()
            .tolist()
        )


embedding_service = (
    EmbeddingService()
)