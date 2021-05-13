from Database import DataBase
import log

database = DataBase.Database()


def search_categories_and_prices(queries: dict):
    query_search = dict()
    query_search["user_id"] = queries["user_id"]
    if queries["category"] == "" and queries["price_range"] == "":
        return [], 200

    if queries["category"] == "":
        log.generate_log_from_search_engine(queries["user_id"], None, None, queries["price_range"])
        query_search["item_price"] = queries["price_range"]
        try:
            result_search = database.search_for_price(query_search)
            return result_search, 200
        except:
            return [], 500

    if queries["price_range"] == "":
        log.generate_log_from_search_engine(queries["user_id"], None, queries["category"], None)
        lista = queries["category"].split(",")
        query_search["category"] = lista
        try:
            result_search = database.search_for_category(query_search)
            return result_search, 200
        except:
            return [], 500

    else:
        log.generate_log_from_search_engine(user_id=queries["user_id"], string_search=None,category=queries["category"],
                                            price_range=queries["price_range"])
        lista = queries["category"].split(",")
        query_search["category"] = lista
        query_search["item_price"] = queries["price_range"]
        try:
            result_search = database.search_for_category_price(query_search)
            return result_search, 200
        except:
            return [], 500

