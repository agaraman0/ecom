from flask import jsonify, Blueprint, make_response, request

from db import Category, Subcategory, db

subcategory = Blueprint("subcategory", __name__, url_prefix="/subcategory/v1")


@subcategory.route('/', methods=['POST'])
def create_subcategory():
    data = request.get_json()
    name = data['name']
    category_id = data['category_id']

    category = Category.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found.'}), 404

    subcategory = Subcategory(name=name, category=category)
    db.session.add(subcategory)
    db.session.commit()

    return jsonify({'message': 'Subcategory created successfully.'})

# Route for retrieving all subcategories
@subcategory.route('/', methods=['GET'])
def get_subcategories():
    subcategories = Subcategory.query.all()

    results = []
    for subcategory in subcategories:
        result = {
            'id': subcategory.id,
            'name': subcategory.name,
            'category_id': subcategory.category_id
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
        return jsonify({'message': 'Subcategory not found.'}), 404

# Route for deleting a subcategory by ID
@subcategory.route('/<int:subcategory_id>', methods=['DELETE'])
def delete_subcategory(subcategory_id):
    subcategory = Subcategory.query.get(subcategory_id)
    if subcategory:
        db.session.delete(subcategory)
        db.session.commit()
        return jsonify({'message': 'Subcategory deleted successfully.'})
    else:
        return jsonify({'message': 'Subcategory not found.'}), 404