from pydantic import BaseModel


class MultimodalNodeResponse(
    BaseModel
):
    text_node_count: int
    image_node_count: int