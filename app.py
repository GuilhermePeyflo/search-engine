from flask import Flask, request, jsonify
from Controller import search

app = Flask(__name__)


@app.route("/search_categories_and_prices/", methods=["GET"])
def search_categories_and_prices():
    queries = dict(category=request.args["category"], price_range=request.args["price_range"], user_id=request.args["user_id"])
    response = search.search_categories_and_prices(queries)
    print(response[0])
    for book_index in range(len(response[0])):
        response[0][book_index]["_id"] = str(response[0][book_index]["_id"])
    return jsonify(response[0])


app.run(debug=True)
