import uuid

from pydantic import BaseModel, Field


class Game(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id", exclude=True)
    title: str = Field(...)
    metacritic_score: int = Field(...)
    must_play: bool = Field(...)
    finished: bool = Field(...)
    genres: list[str] = Field(...)
    labels: list[str] = Field(...)
    fetch_error: bool = Field(...)

    class Config:
        populate_by_name = True  # allow_population_by_field_name
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
