from pymongo import MongoClient


MONGO_URI = "mongodb+srv://nagamohan:RF3EahNbdj6Bo9wN@resume-store.guhgax4.mongodb.net/"
DB_NAME = "gameplan_db"


mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
users_collection = db["users"]
teams_collection = db["teams"]
