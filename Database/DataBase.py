import ast
from datetime import datetime
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


class Database:

    def __init__(self):
        self.conn = MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        self.product_db = self.conn["product_db"]
        self.book = self.product_db["book"]
        self.users_search_db = self.conn["users_search_db"]
        self.search_history = self.users_search_db["search_history"]

    def general_search(self, query: dict) -> tuple:
        """
        Função que aplica a query no db para retornar os livros filtrados
        :param query: query formada para buscas em search
        :return: list, result com a lista de livros após aplicado(s) filtro(s)
        """

        try:
            result = list(self.book.find(query))
            return result, 200
        except Exception as ex:
            return ex.args[0], 500

    def books_by_rating(self) -> tuple:
        """
        Função que busca no db e retorna os livros em ordem de avaliação
        :return: list, result com a lista de livros ordenada pelas avaliações (estrelas)
        """
        try:
            sort = list({'rating': -1}.items())
            result_search = list(self.book.find(sort=sort))
            return result_search, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def books_by_string_search(self, string_search: str) -> tuple:
        """
        Função que busca no db as informações do cadastro de livros e verifica se alguma coincide com a busca do usuário
        :param string_search:
        :return: list, result_search com a lista de livros que contém a busca digitada no front-end
        """
        try:
            if len(string_search) >= 2:
                query = "{'$text': {'$search': '"
                query += str(string_search)
                query += "' }}"
                sort = list({'score':{'$meta':'textScore'}}.items())
                query = ast.literal_eval(query)
                result_search = list(self.book.find(query, sort=sort))
                return result_search, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def latest_books_released(self) -> tuple:
        """
        Função que busca no db os livros e os retorna em ordem de publicação
        :return: list, result_search com a lista de livros ordenada pela data de publicação
        """
        try:
            sort = list({'published_at': -1}.items())
            result_search = list(self.book.find(sort=sort))
            return result_search, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def search_by_id(self, id: str) -> tuple:
        """
        A função recebe o id de um livro selecionado pelo usuário no front-end, conslta esse id no banco para retornar
        todas as informações do livro

        :param id: Id do livro selecionado pelo usuário no front-end
        :return: Tupla com o livro e status code
        """
        try:
            result = list(self.book.find({"_id": ObjectId(id)}))
            return result, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def get_history_searches(self) -> tuple:
        request_body = request.get_json()
        from_dt, to_dt = request_body["initial_date"], request_body["final_date"]
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d')
        to_dt = datetime.strptime(to_dt, '%Y-%m-%d')

        try:
            result = list(self.search_history.find({"created_at": {"$gte": from_dt, "$lte": to_dt}}))
            return result, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500
