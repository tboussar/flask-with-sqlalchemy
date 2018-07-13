# wsgi.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # Heroku does not use .env

from flask import Flask, request, json, render_template
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
    mots = ["Winter", "is", "coming."]
    return render_template('hello.html', titre="Hello", mots=mots)

@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return render_template('products.html', titre="Our Products", products=products)

@app.route('/api/v1/products/<int:id>', methods=['GET'] )
def get_product(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', titre="One Product", product=product)

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
    product = db.session.query(Product).filter(Product.id == id ).delete()
    db.session.commit()
    return 'Product Deleted', 204

@app.route('/api/v1/products/<int:id>', methods=['PATCH'])
def patch_product(id):
    new_name = request.form['name']
    product = db.session.query(Product).filter(Product.id == id).first()
    product.name= new_name
    db.session.commit()
    return 'Product updated', 204



