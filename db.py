from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

product_category = db.Table('product_category',
                            db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                            db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                            )

product_subcategory = db.Table('product_subcategory',
                               db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                               db.Column('subcategory_id', db.Integer, db.ForeignKey('subcategory.id'),
                                         primary_key=True)
                               )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', secondary='category_subcategory', backref='categories',
                                    lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subcategories': [subcategory.to_dict() for subcategory in self.subcategories]
        }


class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    categories = db.relationship('Category', secondary=product_category, backref='products', lazy='dynamic')
    subcategories = db.relationship('Subcategory', secondary=product_subcategory, backref='products', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'categories': [category.to_dict() for category in self.categories],
            'subcategories': [subcategory.to_dict() for subcategory in self.subcategories]
        }


category_subcategory = db.Table('category_subcategory',
                                db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                                db.Column('subcategory_id', db.Integer, db.ForeignKey('subcategory.id'))
                                )
