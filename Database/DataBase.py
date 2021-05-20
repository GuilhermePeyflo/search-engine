import ast
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


class Database:

    def __init__(self):
        self.conn = MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        self.db = self.conn["database_teste"]
        self.search_history = self.db["search_history"]
        self.new_books = self.db["new_books"]

    def general_search(self, query: dict) -> tuple:
        """
        Função que aplica a query no db para retornar os livros filtrados
        :param query: query formada para buscas em search
        :return: list, result com a lista de livros após aplicado(s) filtro(s)
        """

        try:
            result = list(self.new_books.find(query))
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
            result_search = list(self.new_books.find(sort=sort))
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
                result_search = list(self.new_books.find(query, sort=sort))
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
            result_search = list(self.new_books.find(sort=sort))
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
            result = list(self.new_books.find({"_id": ObjectId(id)}))
            return result, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def get_history_searches(self) -> tuple:
        try:
            result = list(self.search_history.find({}))
            return result, 200
        except ConnectionFailure as ex:
            return ex.args[0], 500
