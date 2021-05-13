from pymongo import MongoClient


class Database:

    def __init__(self):
        self.conn = MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        self.db = self.conn["database_teste"]
        self.books_collection = self.db["books"]
        self.search_history = self.db["search_history"]

    def search_for_price(self, queries: dict):
        result_search = ""
        if int(queries["item_price"]) <= 50:
            result_search = self.books_collection.find({"item_price": {"$lte": 50}})
        elif 50 < int(queries["item_price"]) <= 100:
            result_search = self.books_collection.find({"$and": [{"item_price": {"$gt": 50}}, {"item_price": {"$lte": 100}}]})
        elif int(queries["item_price"]) > 100:
            result_search = self.books_collection.find({"item_price": {"$gt": 100}})
        return result_search

    def search_for_category(self, queries: dict):
        if len(queries["category"]) > 1:
            result_search = list(self.books_collection.find({"category": {"$in": queries["category"]}}))
            return result_search
        else:
            print("entrou no ELSE", queries["category"])
            result_search = list(self.books_collection.find({"category": {"$in": queries["category"]}}))
            return result_search

    def search_for_category_price(self, queries: dict):
        results = list()
        search_category = list(self.search_for_category(queries))
        search_price = list(self.search_for_price(queries))
        for book in search_category:
            if book in search_price:
                results.append(book)
        return results
