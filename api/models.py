import uuid
from typing import Optional

from pydantic import BaseModel, Field


class Game(BaseModel):
    # id: uuid.UUID '= Field(default_factory=uuid.uuid4, alias="_id", exclude=True)
    title: str = Field(...)
    metacritic_score: Optional[int] = Field(default=None)
    must_play: Optional[bool] = Field(default=None)
    finished: Optional[bool] = Field(default=None)
    genres: Optional[list[str]] = Field(default=None)
    labels: Optional[list[str]] = Field(default=None)
    fetch_error: Optional[bool] = Field(default=None)

    class Config:
        validate_by_name = True  # allow_population_by_field_name
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Best Game Ever",
                "metacritic_score": 100,
                "must_play": True,
                "finished": False,
                "genres": [
                    "survival-crafting",
                ],
                "labels": [
                    "my custom collection",
                ],
                "fetch_error": False,
            }
        }
