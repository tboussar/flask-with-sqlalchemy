# wsgi.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # Heroku does not use .env

from flask import Flask, request, json
from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema
from schemas import product_schema

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/api/v1/products/<int:id>', methods=['GET'] )
def get_product(id):
    product = db.session.query(Product).get(id)
    return product_schema.jsonify(product)

@app.route('/api/v1/products', methods=['POST'] )
def create_product():
    data = request.form['name']
    product = Product()
    product.name = data
    db.session.add(product)
    db.session.commit()
    return 'Created', 201

@app.route('/api/v1/products/<int:id>', methods=['DELETE'] )
def del_product(id):
    #product= db.session.query(Product).filter(Product.id == id).first()
    #db.session.delete(product)
    #db.session.commit()
    product = db.session.query(Product).filter(Product.id == id ).delete()
    db.session.commit()
    return 'Product Deleted', 204

@app.route('/api/v1/products/<int:id>', methods=['PATCH'])
def patch_product(id):
    new_name = request.form['name']
    product = db.session.query(Product).filter(Product.id == id).first()
    #product = db.session.query(Product).get(id)
    product.name= new_name
    db.session.commit()
    return 'Product updated', 204



