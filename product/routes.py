from flask import jsonify, Blueprint, make_response, request

from db import Product, Category, Subcategory, db

product = Blueprint("product", __name__, url_prefix="/product/v1")

@product.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data['name']
    category_ids = data.get('categories', [])
    subcategory_ids = data.get('subcategories', [])

    product = Product(name=name)
    for category_id in category_ids:
        category = Category.query.get(category_id)
        if category:
            product.categories.append(category)

    for subcategory_id in subcategory_ids:
        subcategory = Subcategory.query.get(subcategory_id)
        if subcategory:
            product.subcategories.append(subcategory)

    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully.'})

# Route for retrieving a product by ID
@product.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        result = {
            'id': product.id,
            'name': product.name,
            'categories': [category.name for category in product.categories],
            'subcategories': [subcategory.name for subcategory in product.subcategories]
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Product not found.'}), 404

# Route for updating a product by ID
@product.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        data = request.get_json()
        product.name = data.get('name', product.name)

        category_ids = data.get('categories', [])
        product.categories.clear()
        for category_id in category_ids:
            category = Category.query.get(category_id)
            if category:
                product.categories.append(category)

        subcategory_ids = data.get('subcategories', [])
        product.subcategories.clear()
        for subcategory_id in subcategory_ids:
            subcategory = Subcategory.query.get(subcategory_id)
            if subcategory:
                product.subcategories.append(subcategory)

        db.session.commit()

        return jsonify({'message': 'Product updated successfully.'})
    else:
        return jsonify({'message': 'Product not found.'}), 404

# Route for deleting a product by ID
@product.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully.'})
    else:
        return jsonify({'message': 'Product not found.'}), 404