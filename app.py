from flask import Flask, make_response, jsonify

from subcategory.routes import subcategory
from category.routes import category
from product.routes import product
from config import config
from db import db
from constants import PATH_NOT_FOUND, SERVER_ERROR, FAILURE_RESPONSE


app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
app.register_blueprint(subcategory)
app.register_blueprint(category)
app.register_blueprint(product)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hello World</h1>'''


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify(FAILURE_RESPONSE), 400)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify(PATH_NOT_FOUND), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify(SERVER_ERROR), 500)


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')