from flask import jsonify, Blueprint, make_response, request

from db import Subcategory, db
from constants import SERVER_ERROR

subcategory = Blueprint("subcategory", __name__, url_prefix="/subcategory/v1")


@subcategory.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@subcategory.route('/', methods=['POST'])
def create_subcategory():
    data = request.get_json()
    name = data.get('name')

    if name:
        subcategory = Subcategory(name=name)
        db.session.add(subcategory)
        db.session.commit()
        return jsonify({'message': 'Subcategory created successfully.', "data": subcategory.to_dict()})

    return jsonify({'message': 'name not found.'}), 404


# Route for retrieving all subcategories
@subcategory.route('/', methods=['GET'])
def get_subcategories():
    subcategories = Subcategory.query.all()

    results = []
    for subcategory in subcategories:
        result = {
            'id': subcategory.id,
            'name': subcategory.name
        }
        results.append(result)

    return jsonify(results)


# Route for retrieving a subcategory by ID
@subcategory.route('/<int:subcategory_id>', methods=['GET'])
def get_subcategory(subcategory_id):
    subcategory = Subcategory.query.get(subcategory_id)
    if subcategory:
        result = {
            'id': subcategory.id,
            'name': subcategory.name,
            'category_id': subcategory.category_id
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Subcategory not found.'}), 400


# Route for deleting a subcategory by ID
@subcategory.route('/<int:subcategory_id>', methods=['DELETE'])
def delete_subcategory(subcategory_id):
    subcategory = Subcategory.query.get(subcategory_id)
    if subcategory:
        db.session.delete(subcategory)
        db.session.commit()
        return jsonify({'message': 'Subcategory deleted successfully.'})
    else:
        return jsonify({'message': 'Subcategory not found.'}), 400


@subcategory.route('/<int:subcategory_id>', methods=['PUT'])
def update_subcategory(subcategory_id):
    subcategory = Subcategory.query.get(subcategory_id)
    if subcategory:
        data = request.get_json()
        name = data.get('name')

        if name:
            subcategory.name = name

        db.session.commit()

        result = {
            'id': subcategory.id,
            'name': subcategory.name
        }

        return jsonify({'message': 'Subcategory updated successfully.', 'subcategory': result})
    else:
        return jsonify({'message': 'Subcategory not found.'}), 400
