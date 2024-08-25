from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        "name": random_cafe.name,
        "map": random_cafe.map_url,
        "image": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })


@app.route("/all", methods=['GET'])
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    list_of_cafes = {"cafes": []}
    for each_cafe in all_cafes:
        cafe = {
            "name": each_cafe.name,
            "map": each_cafe.map_url,
            "image": each_cafe.img_url,
            "location": each_cafe.location,
            "seats": each_cafe.seats,
            "has_toilet": each_cafe.has_toilet,
            "has_wifi": each_cafe.has_wifi,
            "has_sockets": each_cafe.has_sockets,
            "can_take_calls": each_cafe.can_take_calls,
            "coffee_price": each_cafe.coffee_price,
        }
        list_of_cafes["cafes"].append(cafe)
    return jsonify(list_of_cafes)


@app.route("/search", methods=['GET', 'POST'])
def search_cafes():
    location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    all_cafes = result.scalars().all()
    if all_cafes:
        list_of_cafes = {"cafes": []}
        for each_cafe in all_cafes:
            cafe = {
                "name": each_cafe.name,
                "map": each_cafe.map_url,
                "image": each_cafe.img_url,
                "location": each_cafe.location,
                "seats": each_cafe.seats,
                "has_toilet": each_cafe.has_toilet,
                "has_wifi": each_cafe.has_wifi,
                "has_sockets": each_cafe.has_sockets,
                "can_take_calls": each_cafe.can_take_calls,
                "coffee_price": each_cafe.coffee_price,
            }
            list_of_cafes["cafes"].append(cafe)
        return jsonify(list_of_cafes)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
