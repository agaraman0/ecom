from flask import jsonify, Blueprint, make_response, request

from db import Category, db, Subcategory
from constants import SERVER_ERROR

category = Blueprint("category", __name__, url_prefix="/category/v1")


@category.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@category.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name', None)
    subcategory_ids = data.get('subcategories', [])

    if name:
        category = Category(name=name)
        subcategories = Subcategory.query.filter(Subcategory.id.in_(subcategory_ids)).all()
        category.subcategories.extend(subcategories)

        db.session.add(category)
        db.session.commit()

        return jsonify({'message': 'Category created successfully.', "data": category.to_dict()})

    return jsonify({'message': 'Invalid arguments'}), 400


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
            'name': category.name,
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


@category.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found.'}), 404

    data = request.get_json()
    name = data.get('name')
    subcategories = data.get('subcategories')

    # Update category attributes
    if name:
        category.name = name

    # Update subcategories
    if subcategories:
        updated_subcategories = []
        for subcategory_data in subcategories:
            subcategory_id = subcategory_data.get('id')
            subcategory_name = subcategory_data.get('name')
            subcategory = Subcategory.query.get(subcategory_id)
            if subcategory:
                subcategory.name = subcategory_name
                updated_subcategories.append(subcategory)

        category.subcategories = updated_subcategories

    db.session.commit()

    # Retrieve the updated category and subcategories
    updated_category = Category.query.get(category_id).to_dict()
    updated_subcategories = [subcategory.to_dict() for subcategory in category.subcategories]

    # Add subcategories to the category dictionary
    updated_category['subcategories'] = updated_subcategories

    return jsonify(updated_category)
