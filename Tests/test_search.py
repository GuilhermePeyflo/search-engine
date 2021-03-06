from unittest import TestCase, mock
import Controller.search


class TestSearch(TestCase):

    @mock.patch("Controller.search.database.general_search")
    @mock.patch("Controller.search.ast")
    def test_general_search_works(self, mock_ast, mock_db_search):
        filters = dict(price={"min": 0, "max": 50}, category=["Ação", "Fantasia"], language_book="Polish", author=[{"name": "Gil"}, {"lastname": "Berto"}], size={"height":10, "width":12, "length":10})
        mock_ast.literal_eval.return_value = { '$and': [ { '$or': [ {'category': 'Ação'}, {'category': 'Fantasia'}, {'language_book': 'Polish'}, {'author.name': 'Gil'}, {'author.lastname': 'Berto'}, {'size.height': '10'}, {'size.width': '12'}, {'size.length': '10'}]} , { '$and' : [{'item_price': { '$gte' :0}}, {'item_price': { '$lte' :50}} ] }]}
        mock_db_search.return_value = ()

        self.assertEqual(Controller.search.general_search(filters), ())
        self.assertNotEqual(Controller.search.general_search(filters), ([1, 2, 3]))


        filters = dict(category=["Ação", "Fantasia"], language_book="Polish",
                       author=[{"name": "Gil"}, {"lastname": "Berto"}], size={"height": 10, "width": 12, "length": 10})
        mock_ast.literal_eval.return_value = {'$and': [{'$or': [{'category': 'Ação'}, {'category': 'Fantasia'},
                                                                {'language_book': 'Polish'}, {'author.name': 'Gil'},
                                                                {'author.lastname': 'Berto'}, {'size.height': '10'},
                                                                {'size.width': '12'}, {'size.length': '10'}]}]}
        mock_db_search.return_value = ()

        self.assertEqual(Controller.search.general_search(filters), ())
        self.assertNotEqual(Controller.search.general_search(filters), ([1, 2, 3]))

        filters = dict(price={"min": 0, "max": 50})
        mock_ast.literal_eval.return_value = {'$and': [{'item_price': {'$gte': 0}}, {'item_price': {'$lte': 50}}]}
        mock_db_search.return_value = ()

        self.assertEqual(Controller.search.general_search(filters), ())
        self.assertNotEqual(Controller.search.general_search(filters), ([1, 2, 3]))

    @mock.patch("Controller.search.jsonify")
    def test_data_treatment_works(self, mock_json):
        mock_json.side_effect = [None, [], []]
        response = None
        self.assertEqual(Controller.search.data_treatment(response), (None, 400))

        response = ([{"_id": "609ec0b6d2334d102f6561bb"}], 200)
        self.assertEqual(Controller.search.data_treatment(response), ([], 200))

        response = ([], 200)
        self.assertEqual(Controller.search.data_treatment(response), ([], 400))

        response = ([], 500)
        self.assertEqual(Controller.search.data_treatment(response), ("Problema de conexão", 500))



