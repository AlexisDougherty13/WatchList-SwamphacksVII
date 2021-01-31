from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

#OMDB API
apiKey = str(os.getenv("API_KEY"))
data_URL = 'http://www.omdbapi.com/?apikey='+apiKey

#Mongo DB
client = MongoClient(str(os.getenv("MONGO_KEY")))
db = client.Lists
listings = db.Lists