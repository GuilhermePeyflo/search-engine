import ast
from Database import DataBase

database = DataBase.Database()


def general_search(filters: dict) -> list:
    """
    Função que valida os dados enviados pelo front-end, conforme filtros selecionados, levando em consideração o formato
    das informações (dicionario(s), lista, string) e também se o preço foi filtrado ou não.
    :param filters: filtros selecionados pelo usuário
    :return: list, result com a lista de livros filtrados
    """
    query = "{ '$and': [ { '$or': [ "
    price = ""

    for filter in filters:
        if isinstance(filters[filter], dict):
            if filter == "price":
                price += "]} , { '$and' : [{" + "'item_price': { '$gte' :" + f"{filters[filter]['min']}" + "}}, " \
                        "{" + "'item_price': { '$lte' :" + f"{filters[filter]['max']}" + "}} ] }"
            else:
                for item in filters[filter]:
                    query += "{" + f"'{filter}.{item}': '{filters[filter][item]}'" + "}, "
        elif isinstance(filters[filter], list):
            if isinstance(filters[filter][0], dict):
               for item_dict in filters[filter]:
                    for item in item_dict:
                        query += "{" + f"'{filter}.{item}': '{item_dict[item]}'" + "}, "
            else:
                for item in filters[filter]:
                    query += "{" + f"'{filter}': '{item}'" + "}, "
        else:
            query += "{" + f"'{filter}': '{filters[filter]}'" + "}, "

    query = query[0:-2]
    if price != "":
        query += price + "]}"
    else:
        print("else")
        query += "]}] }"
    query = ast.literal_eval(query)
    result = database.general_search(query)
    return result




