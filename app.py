from flask import Flask, request, jsonify
from Controller import search

app = Flask(__name__)


app.run(debug=True)
