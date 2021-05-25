import ast
from Database import DataBase
from flask import jsonify

database = DataBase.Database()


def general_search(filters: dict) -> tuple:
    """
    Função que valida os dados enviados pelo front-end, conforme filtros selecionados, levando em consideração o formato
    das informações (dicionario(s), lista, string) e também se o preço foi filtrado ou não.
    :param filters: filtros selecionados pelo usuário
    :return: list, result com a lista de livros filtrados
    """
    if filters == {}:
        return [], 400

    price = ""
    query = ""

    try:
        filters['category']
        query = "{ '$and': [ { '$or': [ "


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
            query += "]}] }"

    except:
        for filter in filters:
            query = "{ '$and' : [{" + "'item_price': { '$gte' :" + f"{filters[filter]['min']}" + "}}, " \
                                "{" + "'item_price': { '$lte' :" + f"{filters[filter]['max']}" + "}} ] }"

    query = ast.literal_eval(query)
    result = database.general_search(query)
    return result


def data_treatment(response):
    """
    A função recebe uma tupla com as lista de dados retornados do banco e o status code da requisição e verifica os
    dados para enviar ao front-end

    Os dois returns com 400 se referem ao recebimento de uma string vazia (primeiro) e uma lista vazia (último). MAS
    é esperado que não ocorra porque o front não deve enviar filtros vazios.
    :param response: Resposta retornado das funções de consulta no banco de dados, com lista de items pesquisados e
    status code da requisição
    :return: Tupla com uma lista de dados e status code da request
    """
    if response is None:
        return jsonify(response), 400
    if response[1] == 200 and len(response[0]) > 0:
        for book_index in range(len(response[0])):
            response[0][book_index]["_id"] = str(response[0][book_index]["_id"])
        return jsonify(response[0]), 200
    elif response[1] == 500:
        return "Problema de conexão", 500
    else:
        return jsonify(response[0]), 400
