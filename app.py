from flask import Flask, request, jsonify
from Controller import search
from ast import literal_eval
import log
from Database import DataBase

app = Flask(__name__)


@app.route("/general_search", methods=["POST"])
def general_search():
    """
    A função recebe do front-end um json com os filtros e realiza a busca no db.
    :return: tuple, response com a lista de livros filtrados
    """
    filters = request.data.decode("utf-8")
    filters = literal_eval(filters)
    log.generate_log_from_search_engine(filters)
    #talvez um pop aqui seja necessário...
    response = search.general_search(filters)
    if response:
        for book_index in range(len(response)):
            response[book_index]["_id"] = str(response[book_index]["_id"])
        return jsonify(response), 200
    return response, 500


@app.route("/books_by_rating")
def books_by_rating():
    """
    A função é chamada na página inicial do front-end quando acessado o site.
    :return: tuple, response com a lista de livros ordenada pelas avaliações (estrelas)
    """
    response = DataBase.Database().books_by_rating()
    if response:
        for book_index in range(len(response)):
            response[book_index]["_id"] = str(response[book_index]["_id"])
        return jsonify(response), 200
    return response, 500


@app.route("/books_by_string_search")
def books_by_string_search():
    """
    A função recebe do front-end uma string digitada pelo usuário e realiza a busca no db.
    :return: tuple, response com a lista de livros que contém a busca digitada no front-end
    """
    string_search = request.args['search']
    response = DataBase.Database().books_by_string_search(string_search)
    if response:
        for book_index in range(len(response)):
            response[book_index]["_id"] = str(response[book_index]["_id"])
        return jsonify(response), 200
    return response, 500


@app.route("/books_by_released")
def books_by_released():
    """
    A função é chamada na página inicial do front-end quando acessado o site.
    :return: tuple, response com a lista de livros ordenada pela data de publicação.
    """
    response = DataBase.Database().latest_books_released()
    if response:
        for book_index in range(len(response)):
            response[book_index]["_id"] = str(response[book_index]["_id"])
        return jsonify(response), 200
    return response, 500


app.run(debug=True)
