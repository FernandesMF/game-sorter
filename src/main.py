# run with:
# python -m uvicorn main:app --reload
# with logging (for debugs)
# python -m uvicorn main:app --reload --log-config=log_conf.yaml

import logging
from contextlib import asynccontextmanager
from typing import Annotated, Any, Literal, Union

import certifi
from dotenv import dotenv_values
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict
from pymongo import DESCENDING, MongoClient

from .models import Game

config = dotenv_values(".env")
db_vars = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_vars["client"] = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
    db_vars["db"] = db_vars["client"][config["DB_NAME"]]
    db_vars["collection"] = db_vars["db"].get_collection("games")
    print("Connected to the MongoDB database!")

    yield

    db_vars["client"].close()


logger = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():

    return {"message": db_vars.__str__()}


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


# TODO implement 'hot picks' filter logic
@app.get(
    "/games", response_description="List games with filter", response_model=list[Game]
)
async def list_games(
    filter_params: Annotated[GamesFilterParams, Query()],
) -> list[Game]:

    results: list[dict] = []
    filter_: dict[str:Any] = {}
    params_dict = filter_params.model_dump()
    sort_field = params_dict["sort_by"]
    params_dict.pop("sort_by")

    for param_name in params_dict.keys():

        # if field is of bool type an equals none, dont include it in the filter
        if filter_params.model_fields[param_name].annotation == Union[bool, None]:
            if params_dict[param_name] is None:
                continue
        # for other types, dont include the value in the filter in case it has a boolean value of false
        if not params_dict[param_name]:
            continue
        # for list fields, use 'in' operator to search for any value
        if isinstance(params_dict[param_name], list):
            filter_.update(
                {param_name: {"$in": filter_params.model_dump()[param_name]}}
            )
            continue
        filter_.update({param_name: filter_params.model_dump()[param_name]})

    results = list(
        db_vars["collection"].find(filter_, {"_id": 0}, sort=[(sort_field, DESCENDING)])
    )  # suppress the '_id' field
    return results


# @app.get("/authtest")
# async def authtest():

#     payload = {
#         'inUserName': os.environ["username"],
#         'inUserPass': os.environ["password"],
#     }

#     with requests.Session() as s:
#         p = s.post(, data=payload)
#         # print the HTML returned or something more intelligent to see if it's a successful login page.
#         print(p.text)

#         # An authorised request.
#         r = s.get('A protected web page URL')
#         print(r.text)


favicon_path = "favicon.ico"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
