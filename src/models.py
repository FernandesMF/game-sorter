import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Label(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id", exclude=True)
    description: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6g",
                "description": "my custom collection",
            }
        }


class Genre(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id", exclude=True)
    description: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                "description": "survival-crafting",
            }
        }


class Game(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id", exclude=True)
    title: str = Field(...)
    metacritic_score: int = Field(...)
    must_play: bool = Field(...)
    finished: bool = Field(...)
    genres: list[Genre] = Field(...)
    labels: list[Label] = Field(...)
    fetch_error: bool = Field(...)

    class Config:
        populate_by_name = True  # allow_population_by_field_name
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Best Game Ever",
                "metacritic_score": 100,
                "must_play": True,
                "finished": False,
                "genres": [
                    {
                        "_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                        "description": "survival-crafting",
                    }
                ],
                "labels": [
                    {
                        "_id": "066de609-b04a-4b30-b46c-32537c7f1f6g",
                        "description": "my custom collection",
                    }
                ],
                "fetch_error": False,
            }
        }


# class GameGenre(BaseModel):
#     game_id: str = Field(...)
#     label_id: str = Field(...)

#     class Config:
#         populate_by_name = True
#         schema_extra = {
#             "example": {
#                 "game_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "label_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
#             }
#         }


# class GameLabel(BaseModel):
#     game_id: str = Field(...)
#     label_id: str = Field(...)

#     class Config:
#         populate_by_name = True
#         schema_extra = {
#             "example": {
#                 "game_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "label_id": "066de609-b04a-4b30-b46c-32537c7f1f6g",
#             }
#         }
