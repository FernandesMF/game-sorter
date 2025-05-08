import os
import time
from contextlib import asynccontextmanager

import certifi
from fastapi import FastAPI
import requests
import motor
from dotenv import dotenv_values
from pymongo import MongoClient
import json

from .models import Game


config = dotenv_values(".env")
db_vars = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_vars
    db_vars["client"] = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
    db_vars["db"] = db_vars["client"][config["DB_NAME"]]
    db_vars["collection"] = db_vars["db"].get_collection('games')
    print("Connected to the MongoDB database!")

    yield

    db_vars["client"].close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():    

    return {"message": db_vars.__str__()}


# python -m uvicorn main:app --reload


#TODO implement filtering based on variable input fields
@app.get("/games", response_description="List games with filter")#, response_model=list[Game])
async def list_games(name: str=None):# -> list[Game]:

    results = []
    filter = {}
    if name:
        filter.update({"name": name})

    #TODO fix return type (type hints, cast results, etc)
    # results = db_vars["collection"].find(filter)
    results = list(db_vars["collection"].find({}))
    
    return results.__str__()


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
