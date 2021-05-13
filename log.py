from datetime import datetime
from Database import DataBase


def generate_log_from_search_engine(user_id: str = None,
                                    string_search: str = None,
                                    category: str = None,
                                    price_range: int = None):
    dict_persist = dict()
    dict_persist["created_at"] = datetime.now()
    if user_id:
        dict_persist["user_id"] = user_id
    if string_search:
        dict_persist["string_search"] = string_search
    if category:
        dict_persist["category"] = category
    if price_range:
        dict_persist["price_range"] = price_range

    execute = DataBase.Database().search_history.insert_one(dict_persist)
    if execute.inserted_id:
        return True
