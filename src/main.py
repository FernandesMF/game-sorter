import os

from fastapi import FastAPI
import requests
from dotenv import dotenv_values
from pymongo import MongoClient



app = FastAPI()

config = dotenv_values(".env")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


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

    


