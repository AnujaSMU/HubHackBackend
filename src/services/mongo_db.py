import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

load_dotenv()

client = MongoClient(os.getenv("URI_MONGO"))#, server_api=ServerApi('1'))
db = client["ISANS"]

try:
    client.admin.command('ping')
    print("Pinged deployment. Successfully connected to MongoDB!")
except Exception as e:
    print(e)
