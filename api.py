import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/',methods=['GET'])
def home():
    return ''''''

@app.errorhandler(404)
def missing_page(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
