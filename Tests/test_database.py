from unittest import TestCase, mock
from flask import request
from Database import DataBase




class TestDatabase(TestCase):

    @mock.patch("Database.DataBase.Database.new_books", create=True)
    def test_general_search_works(self, mock_new_books):
        with mock.patch.object(DataBase.Database, "__init__", lambda x: None) as mock_db:
            mock_new_books.find.return_value = []

            self.assertEqual(DataBase.Database().general_search({}), ([], 200))


        self.assertEqual(DataBase.Database().general_search("socorro"), ('filter must be an instance of dict, '
                                                                         'bson.son.SON, or any other type that '
                                                                         'inherits from collections.Mapping', 500))

    @mock.patch("Database.DataBase.Database.new_books", create=True)
    def test_books_by_rating_works(self, mock_new_books):
        with mock.patch.object(DataBase.Database, "__init__", lambda x: None) as mock_db:
            mock_new_books.find.return_value = []
            self.assertEqual(DataBase.Database().books_by_rating(), ([], 200))

    @mock.patch("Database.DataBase.Database.new_books", create=True)
    def test_books_by_string_search_works(self, mock_new_books):
        with mock.patch.object(DataBase.Database, "__init__", lambda x: None) as mock_db:
            mock_new_books.find.return_value = []
            self.assertEqual(DataBase.Database().books_by_string_search("Pedro"), ([], 200))

    @mock.patch("Database.DataBase.Database.new_books", create=True)
    def test_latest_books_released_works(self, mock_new_books):
        with mock.patch.object(DataBase.Database, "__init__", lambda x: None) as mock_db:
            mock_new_books.find.return_value = []
            self.assertEqual(DataBase.Database().latest_books_released(), ([], 200))

    @mock.patch("Database.DataBase.Database.conn", create=True)
    @mock.patch("Database.DataBase.Database.new_books", create=True)
    def test_search_by_id_works(self, mock_new_books, mock_conn):
        with mock.patch.object(DataBase.Database, "__init__", lambda x: None) as mock_db:
            mock_new_books.find.return_value = []
            self.assertEqual(DataBase.Database().search_by_id("609ec0b6d2334d102f6561bb"), ([], 200))

    @mock.patch("Database.DataBase.Database.search_history", create=True)
    @mock.patch("Database.DataBase.datetime")
    @mock.patch("Database.DataBase.request")
    def test_get_history_searches_works(self, mock_request, mock_datetime, mock_search_history):
        mock_request.request.return_value = mock.Mock()
        mock_request.request.get_json().return_value = {"initial_date", "final_date"}
        mock_datetime.strptime.return_value = '%Y-%m-%d'

        with mock.patch.object(DataBase.Database, "__init__", lambda x: None) as mock_db:
            mock_search_history.find.return_value = []

            self.assertEqual(DataBase.Database().search_by_id(""), ([], 200))
