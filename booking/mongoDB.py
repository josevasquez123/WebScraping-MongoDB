from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

class MongoDB():
    def __init__(self):
        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        connection_string = f"mongodb+srv://m220student:{password}@mflix.xrjwyfu.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(connection_string)
        self.hotel_db = self.client.hotel
        self.hotel_info = self.hotel_db.hotel_info

    def insert_documents(self, hotel_one_page):
        docs = []
        for hotel_info in hotel_one_page:
            doc = {'hotel_name': hotel_info[0],'hotel_price': hotel_info[1],'hotel_score':hotel_info[2]}
            docs.append(doc)
        self.hotel_info.insert_many(docs)
    



