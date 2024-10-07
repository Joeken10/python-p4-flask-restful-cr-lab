#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Resource to handle /plants route
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        data = request.get_json()

        # Validate that the required fields are provided
        if not data.get('name') or not data.get('image') or not data.get('price'):
            return {"error": "Name, image, and price are required."}, 400

        # You can also check if price is a valid float
        try:
            price = float(data['price'])
        except ValueError:
            return {"error": "Price must be a number."}, 400

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=price
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201

# Resource to handle /plants/<id> route
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)

        if plant:
            return jsonify(plant.to_dict())
        else:
            return {"error": "Plant not found"}, 404

# Add resources to the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
