import os # Used to read environment variables
from dotenv import load_dotenv # Used to load environment variables from a .env file
from pymongo import MongoClient # Used to connect to MongoDB


load_dotenv() # Load environment variables from a .env file

MONGO_URI = os.getenv("MONGO_URI") # getting mongo uri from env file

client = MongoClient(MONGO_URI) # connecting fastapi to mongodb

db = client["todo_db"] # Accessing the "todo_db" database in mongodb if it doesn't exist it will be created automatically
todo_collection = db["todos"] # Accessing the "todos" collection in the "todo_db" database if it doesn't exist it will be created automatically
user_collection = db["User"]