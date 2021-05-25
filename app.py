from flask import Flask, request
import Controller.search
from Controller import search
from ast import literal_eval
import log_for_search
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
    log_for_search.generate_log_from_search_engine(filters)
    response = search.general_search(filters)
    return Controller.search.data_treatment(response)


@app.route("/books_by_rating")
def books_by_rating():
    """
    A função é chamada na página inicial do front-end quando acessado o site.
    :return: tuple, response com a lista de livros ordenada pelas avaliações (estrelas)
    """
    response = DataBase.Database().books_by_rating()
    return Controller.search.data_treatment(response)


@app.route("/books_by_string_search")
def books_by_string_search():
    """
    A função recebe do front-end uma string digitada pelo usuário e realiza a busca no db.
    :return: tuple, response com a lista de livros que contém a busca digitada no front-end
    """
    string_search = request.args['search']
    log_for_search.generate_log_from_search_engine({"string_search": string_search})
    response = DataBase.Database().books_by_string_search(string_search)
    return Controller.search.data_treatment(response)


@app.route("/books_by_released")
def books_by_released():
    """
    A função é chamada na página inicial do front-end quando acessado o site.
    :return: tuple, response com a lista de livros ordenada pela data de publicação.
    """
    response = DataBase.Database().latest_books_released()
    return Controller.search.data_treatment(response)


@app.route("/selected_book")
def selected_book():
    book_id = request.args["product_id"]
    response = DataBase.Database().search_by_id(book_id)
    return Controller.search.data_treatment(response)


@app.route("/get_all_searches", methods=["POST"])
def get_all_searches():
    response = DataBase.Database().get_history_searches()
    return Controller.search.data_treatment(response)

app.run(debug=True)
