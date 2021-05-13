from pymongo import MongoClient


class Database:

    def __init__(self):
        self.conn = MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        self.db = self.conn["database_teste"]
        self.books_collection = self.db["books"]
        self.search_history = self.db["search_history"]
