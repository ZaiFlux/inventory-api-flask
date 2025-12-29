from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Inventory Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'value': self.value
        }

    def __repr__(self):
        return f"<Item {self.item_name}>"

# Create database tables
with app.app_context():
    db.create_all()

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Inventory Management System"})

# Get all items
@app.route("/items", methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify({"items": [item.to_dict() for item in items]})

# Get a single item by ID
@app.route("/item/<int:item_id>", methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.to_dict())
    else:
        return jsonify({"error": "Item not found"}), 404

# Add a new item
@app.route("/items", methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or not all(k in data for k in ('item_name', 'quantity', 'value')):
        return jsonify({"error": "Missing data"}), 400
    new_item = Item(
        item_name=data['item_name'],
        quantity=data['quantity'],
        value=data['value']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

# Update an existing item
@app.route("/item/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get(item_id)
    if item:
        item.item_name = data.get('item_name', item.item_name)
        item.quantity = data.get('quantity', item.quantity)
        item.value = data.get('value', item.value)
        db.session.commit()
        return jsonify(item.to_dict())
    else:
        return jsonify({"error": "Item not found"}), 404

# Delete an item
@app.route("/item/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"})
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
