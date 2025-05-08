from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
import certifi
config = dotenv_values(".env")
app = FastAPI()
app.mongodb_client = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
app.database = app.mongodb_client[config["DB_NAME"]]
collection = app.database.get_collection('games')
collection.count_documents({"title": "Best Game Ever"})
# db = app.mongodb_client.get_database(config['DB_NAME'])
