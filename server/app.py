#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


@app.route('/bakeries', methods=['GET'])
def bakeries():
    response = make_response(
        jsonify([bakery.to_dict() for bakery in Bakery.query.all()]),  # Fetch and serialize in one line
        200,
        {"Content-Type": "application/json"}
    )
    return response

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    # Fetch the specific bakery by its ID
    bakery = Bakery.query.get(id)
    # Create a response with the bakery's details, including baked goods
    response = make_response(
        jsonify({
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'baked_goods': [baked_good.to_dict() for baked_good in bakery.baked_goods]  # Assuming baked_goods is a relationship
        }),
        200,
        {"Content-Type": "application/json"}
    )
    
    return response



@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()  # Sort by price descending
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()  # Fetch the most expensive item
    return jsonify(baked_good.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
