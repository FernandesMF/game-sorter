import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Game(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    metacritic_score: int = Field(...)
    must_play: bool = Field(...)
    finished: bool = Field(...)
    fetch_error: bool = Field(...)

    class Config:
        populate_by_name = True  #allow_population_by_field_name
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Best Game Ever",
                "metacritic_score": 100,
                "must_play": True,
                "finished": False,
                "fetch_error": False,                
            }
        }


class Genre(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    description: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
                "description": "Survival-crafting",
            }
        }


class GameGenre(BaseModel):
    game_id: str = Field(...)
    label_id: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "game_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "label_id": "066de609-b04a-4b30-b46c-32537c7f1f6f",
            }
        }


class Label(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    description: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6g",
                "description": "my custom collection",
            }
        }


class GameLabel(BaseModel):
    game_id: str = Field(...)
    label_id: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "game_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "label_id": "066de609-b04a-4b30-b46c-32537c7f1f6g",
            }
        }