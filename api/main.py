# run with:
# python -m uvicorn main:app --reload
# with logging (for debugs)
# python -m uvicorn main:app --reload --log-config=log_conf.yaml

import logging
from contextlib import asynccontextmanager
from os import getenv
from typing import Annotated, Any, Literal, Union

import certifi
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from pymongo import DESCENDING, MongoClient
from pymongo.collection import Collection

import epic, metacritic
from models import Game

db_vars: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_vars["client"] = MongoClient(getenv("ATLAS_URI", ''), tlsCAFile=certifi.where())
    db_vars["db"] = db_vars["client"][getenv("DB_NAME", '')]
    db_vars["collection"] = db_vars["db"].get_collection("games")
    print("Connected to the MongoDB database!")

    yield

    db_vars["client"].close()


logger = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():

    return {"message": db_vars.__str__()}


#TODO check error handling
#TODO check duplicate entry avoidance
@app.get("/ingest")
async def data_ingest_flow():

    if not await epic.check_egs_auth():
        return "Auth with EGS is not correctly set up. Make a request to '/epic' and solve any issues."

    title_list = await epic.get_epic_games_list()
    problems = list[tuple]

    for t in title_list:
        try :
            data = await metacritic.get_metacritic_data(t)
        except Exception as e:
            logger.info(f"Problem processing title {t}, skipping")
            problems.append((t, e))  #FIXME this seems wrong...
            continue

        game_entry = Game(title=t, **data)

        collection: Collection = db_vars["collection"]
        if not collection.find_one({'title': t}, {"_id": 0}):
            collection.insert_one(document=dict(game_entry))

    return f"Ingestion flow complete! Problems with the following titles: {problems}"
    

class GamesFilterParams(BaseModel):
    sort_by: Literal["title", "score"] = "score"
    title: str | None = None
    score: Annotated[int | None, Query(ge=0, le=100, default=None)]
    labels: list[str] = []
    genre: list[str] = []
    must_play: bool | None = None
    finished: bool | None = None
    hot_picks: bool | None = None
    fetch_error: bool | None = None
    model_config = ConfigDict(
        extra="forbid"
    )  # forbid different fields (than the ones we are setting)


@app.get(
    "/games",
    response_description="Filter and list game entries",
    response_model=list[Game],
)
async def list_games(
    filter_params: Annotated[GamesFilterParams, Query()],
) -> list[Game]:

    results: list[dict] = []
    filter_: dict[str, Any] = {}
    params_dict = filter_params.model_dump()
    sort_field = params_dict["sort_by"]
    params_dict.pop("sort_by")

    for param_name in params_dict.keys():

        # if field is of bool type and is unset, dont include it in the filter
        if filter_params.model_fields[param_name].annotation == Union[bool, None]:
            if params_dict[param_name] is None:
                continue
        # for other types, dont include the value in the filter in case it has a boolean value of false
        elif not params_dict[param_name]:
            continue
        # for list fields, use 'in' operator to search for any value
        if isinstance(params_dict[param_name], list):
            filter_.update(
                {param_name: {"$in": filter_params.model_dump()[param_name]}}
            )
            continue
        filter_.update({param_name: filter_params.model_dump()[param_name]})

    results = list(
        db_vars["collection"].find(
            filter_,
            {"_id": 0},
            sort=[(sort_field, DESCENDING)],
        )  # suppress the '_id' field from the game entries
    )
    # Convert MongoDB documents to Game instances
    return [Game(**doc) for doc in results]


app.include_router(epic.router, prefix="/epic")
app.include_router(metacritic.router, prefix="/metacritic")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = "favicon.ico"
    return FileResponse(favicon_path)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# app.include_router(api.router)