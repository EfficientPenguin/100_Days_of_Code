'''
    Day 66 - Build your own RESTful API. The starting project files were manually typed here.
'''

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from dotenv import load_dotenv

import random
import os

# --- Load in the .env varas
load_dotenv()

# --- Constants
DELETE_API_KEY = os.environ.get('DELETE_API_KEY')

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Cafe table config
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
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
        # return {
        #     'id': self.id,
        #     'name': self.name,
        #     'map_url': self.map_url,
        #     'img_url': self.img_url,
        #     'location': self.location,
        #     'seats': self.seats,
        #     'has_toilet': self.has_toilet,
        #     'has_wifi': self.has_wifi,
        #     'has_sockets': self.has_sockets,
        #     'can_take_calls': self.can_take_calls,
        #     'coffee_price': self.coffee_price,
        # }

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Create a few entries in teh db
    # new_entry = Cafe(
    #     name = "Best Cafe",
    #     map_url = "some_url",
    #     img_url = "the_img_url",
    #     location = "some location",
    #     seats = "144",
    #     has_toilet = True,
    #     has_wifi = False,
    #     has_sockets = True,
    #     can_take_calls = True,
    #     coffee_price = "4.95"
    # )
    # db.session.add(new_entry)
    # db.session.commit()

    # Get the entries from the database
    cafes = db.session.execute(db.select(Cafe)).scalars().all()

    for cafe in cafes:
        print(cafe.name)


    return render_template("index.html")

@app.route('/random', methods=['GET'])
def rand_cafe():
    # Get a random cafe to display on this page
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    rand_cafe = random.choice(all_cafes)

    response = jsonify(rand_cafe.to_dict())

    return response.json

@app.route('/all', methods=['GET'])
def all_cafes():
    ''' Return all the cafes in teh database as a JSON.'''
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()

    return {"cafes":[jsonify(cafe.to_dict()).json for cafe in all_cafes]}

@app.route('/search', methods=["GET"])
def search_location():
    ''' Search for cafes that have a loc=LOCATION. The user will pass loc as a parameter in the URL.'''
    loc = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
    all_cafes_at_loc = result.scalars().all()

    if all_cafes_at_loc:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes_at_loc])
    return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})

# HTTP GET - Read Record

# HTTP POST - Create Record
@app.route('/add', methods=["POST"])
def add_cafe():
    ''' Add a cafe without using WTForms. Use POST to get the data and create a new cafe entry.
        Return a success as JSON to show the user the cafe was successfully added.'''
    new_cafe = Cafe(
        name = request.form.get('name'),
        map_url = request.form.get('map_url'),
        img_url = request.form.get('img_url'),
        location = request.form.get('location'),
        has_sockets = bool(request.form.get('has_sockets')),
        has_toilet = bool(request.form.get('has_toilet')),
        has_wifi = bool(request.form.get('has_wifi')),
        can_take_calls = bool(request.form.get('can_take_calls')),
        seats = request.form.get('seats'),
        coffee_price = request.form.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"Success": "Successfully added the new cafe."})

# HTTP PUT/PATCH = Update Record
@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    ''' Update the coffee_price given the Cafe's ID field. Use PATCH request to only update the coffee price;
        the rest of the fields remain unchanged.'''
    try:
        # Get the att to update using PATCH
        new_price = request.args.get('coffee_price')
        # Get the cafe by the id
        cafe = db.session.get(Cafe, cafe_id)
    except AttributeError:
        return jsonify(error={"Not Found": f"Sorry a cafe with id={cafe_id} was not found in the database."}), 404
    else:
        # Set the coffee_price to the new price
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(success={"Success": "Successfully updated the price."}), 200
    
# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    ''' DELETE a cafe in the database, but only if you know the secret API-key'''
    api_key = request.args.get('api-key')

    if api_key == DELETE_API_KEY:
        try:
            cafe = db.session.get(Cafe, cafe_id)
        except AttributeError:
            return jsonify(error={"ID not found": f"The cafe with id={cafe_id} was not found in the database."}), 404
        if cafe != None:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success={"Deleted record": f"The cafe with id={cafe_id} was deleted from the database."}), 200
        return jsonify(error={"ID not found": f"The cafe with id={cafe_id} was not found in the database."}), 404
    
    return jsonify({"error": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

if __name__ == "__main__":
    app.run(debug=True)