from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define Plant model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

# Route to get a plant by ID
@app.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": plant.price,
        "is_in_stock": plant.is_in_stock
    })

# Route to update a plant's stock status
@app.route("/plants/<int:id>", methods=["PATCH"])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    data = request.get_json()
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]

    db.session.commit()

    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": plant.price,
        "is_in_stock": plant.is_in_stock
    })

# Route to delete a plant
@app.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    db.session.delete(plant)
    db.session.commit()

    return "", 204  # No content response

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5555)
