from datetime import datetime
from Database import DataBase

# class Database:
#
#     def __init__(self):
#         self.conn = MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
#         self.db = self.conn["database_teste"]
#
# teste = Database()
# ### Criar uma única vez
# ###  db_search_history = teste.db.create_collection("search_history")
# db_search_history = teste.db["search_history"]
    #OU RECEBE A STRING
    #OU RECEBE CATEGORY E/OU PRICE_RANGE


def generate_log_from_search_engine(user_id: str = None,
                                    string_search: str = None,
                                    category: str = None,
                                    price_range: int = None):
    print(category)
    dict_persist = dict()
    dict_persist["created_at"] = datetime.now()
    if user_id:
        dict_persist["user_id"] = user_id
    if string_search:
        dict_persist["string_search"] = string_search
    if category:
        print(category)
        dict_persist["category"] = category
    if price_range:
        dict_persist["price_range"] = price_range

    print(dict_persist)
    execute = DataBase.Database().search_history.insert_one(dict_persist)
    if execute.inserted_id:
        print(True)

# generate_log_from_search_engine(price_range=50, category = 'LINGUAS')
# # PARA APRESENTAR
# resultado = db_search_history.find({})
# dict_dados = pd.DataFrame(resultado)
# dict_dados = dict_dados.astype(str).to_json(orient="records")
# print(dict_dados)

