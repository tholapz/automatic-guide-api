from pydantic import BaseModel
from ModelEnum import ModelEnum

class Item(BaseModel):
    prompt: str
    url: str
    model: ModelEnum
