import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
import requests
import motor
from dotenv import dotenv_values
from pymongo import MongoClient


config = dotenv_values(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

    yield

    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/")

# python -m uvicorn main:app --reload

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
