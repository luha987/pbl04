from flask import Flask, jsonify, request
from flask_cors import CORS  # Untuk memungkinkan akses lintas domain
from peewee import *

app = Flask(__name__)
CORS(app)  # Aktifkan CORS untuk mengizinkan akses dari frontend
database = SqliteDatabase('carsweb.db')


class BaseModel(Model):
    class Meta:
        database = database


class TBCars(BaseModel):
    id = AutoField()
    carname = TextField()
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()


def create_tables():
    with database:
        database.create_tables([TBCars])


@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = list(TBCars.select().dicts())
    return jsonify(cars)


@app.route('/api/cars', methods=['POST'])
def create_car():
    data = request.json
    car = TBCars.create(
        carname=data.get('carname'),
        carbrand=data.get('carbrand'),
        carmodel=data.get('carmodel'),
        carprice=data.get('carprice')
    )
    return jsonify({"id": car.id}), 201


@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = TBCars.get_or_none(TBCars.id == car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    data = request.json
    car.carname = data.get('carname', car.carname)
    car.carbrand = data.get('carbrand', car.carbrand)
    car.carmodel = data.get('carmodel', car.carmodel)
    car.carprice = data.get('carprice', car.carprice)
    car.save()
    return jsonify({"message": "Car updated"})


@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = TBCars.get_or_none(TBCars.id == car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    car.delete_instance()
    return jsonify({"message": "Car deleted"})


if __name__ == '__main__':
    create_tables()
    app.run(port=9000, debug=True)
