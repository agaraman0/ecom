from flask import jsonify, Blueprint, make_response, request

from db import Product, Category, Subcategory, db

from constants import ROWS_PER_PAGE, SERVER_ERROR

product = Blueprint("product", __name__, url_prefix="/product/v1")


@product.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@product.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data['name']
    category_ids = data['category_ids']
    subcategory_ids = data['subcategory_ids']

    # Retrieve categories and subcategories
    categories = Category.query.filter(Category.id.in_(category_ids)).all()
    subcategories = Subcategory.query.filter(Subcategory.id.in_(subcategory_ids)).all()

    product = Product(name=name)
    product.categories = categories
    product.subcategories = subcategories

    db.session.add(product)
    db.session.commit()

    # Retrieve the product with category and subcategory details
    product_data = Product.query.get(product.id).to_dict()

    return jsonify(product_data)


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
        return jsonify({'message': 'Product not found.'}), 400


# paginated product api to reduce load and improve performance of product retrieving api
@product.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    products = Product.queryquery.paginate(page=page, per_page=ROWS_PER_PAGE)

    results = []

    for product in products:
        result = {
            'id': product.id,
            'name': product.name,
            'categories': [category.name for category in product.categories],
            'subcategories': [subcategory.name for subcategory in product.subcategories]
        }
        results.append(result)

    return jsonify(results)


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


# Search for products by name, category, and subcategories
@product.route('/search', methods=['GET'])
def search_products():
    name = request.args.get('name')
    category_id = request.args.get('category_id')
    subcategory_id = request.args.get('subcategory_id')

    products = Product.query

    if name:
        products = products.filter(Product.name.ilike(f'%{name}%'))
    if category_id:
        products = products.filter(Product.categories.any(Category.id == category_id))
    if subcategory_id:
        products = products.filter(Product.subcategories.any(Subcategory.id == subcategory_id))

    results = []
    for product in products:
        result = product.to_dict()
        results.append(result)

    return jsonify(results)