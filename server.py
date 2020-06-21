import flask
from flask import request, jsonify
from data.gags import gagData
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/',methods=['GET'])
def home():
    return """<h1>Toontown Battle Simulator</h1><p>Work in progress.</p><img src="bugle.png" alt="Cake" width="128" height="128">"""

@app.route('/gags', methods=['GET'])
def view_gags():
    if 'track' in request.args:
        return jsonify([gag for gag in gagData if gag['track'] == request.args['track']])
    if 'name' in request.args:
        return jsonify([gag for gag in gagData if gag['name'] == request.args['name']])

    return jsonify(gagData)

@app.route('/gags',methods=['POST'])
def new_gag():
    if not request.json or not 'name' in request.json:
        abort(400)
    gag = request.json
    gagData.append(gag)
    return jsonify(gag), 201

@app.route('/submit',methods=['POST'])
def submit():
    print(request)
    if request.json:
        data = request.json
        # if 'plan' not in data or 'toons' not in data or 'cogs' not in data:
        #     abort(400)
        # request.
        # SubmitAction(data)

@app.errorhandler(404)
def missing_page(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
