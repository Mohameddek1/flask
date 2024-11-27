from flask import Blueprint, request, jsonify
from models import db, Customer

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/', methods=["POST"])
def add_customer():
    data = request.json
    customer = Customer(name=data['name'], email=data['email'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "Customer added successfully!"}), 201