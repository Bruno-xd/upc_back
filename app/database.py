from pymongo import MongoClient

MONGO_URL = "mongodb+srv://admin:admin123@dengue.fjrsqhl.mongodb.net/?appName=dengue"

client = MongoClient(MONGO_URL)

db = client["dengue_db"]

predicciones_collection = db["predicciones"]