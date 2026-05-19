from pydantic import BaseModel

class IndexingResponse(
    BaseModel
):
    collection_name: str
    indexed_points: int