from flask import jsonify, Blueprint, make_response, request

from db import Category, db

category = Blueprint("category", __name__, url_prefix="/category/v1")

@category.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data['name']
    
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully.'})

# Route for retrieving all categories
@category.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()

    results = []
    for category in categories:
        result = {
            'id': category.id,
            'name': category.name
        }
        results.append(result)

    return jsonify(results)

# Route for retrieving a category by ID
@category.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category:
        result = {
            'id': category.id,
            'name': category.name
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Category not found.'}), 404

# Route for deleting a category by ID
@category.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully.'})
    else:
        return jsonify({'message': 'Category not found.'}), 404