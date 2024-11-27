from flask import Blueprint, request, jsonify
from models import db, CreditCard, aes_encrypt, aes_decrypt
from config import config

credit_card_bp = Blueprint('credit', __name__)

@credit_card_bp.route('/', methods=["POST"])
def add_card():
    data = request.json
    encrypted_card_number = aes_encrypt(data['card_number'], config.AES_KEY)
    encrypted_cvv = aes_encrypt(data['cvv'], config.AES_KEY)
    encrypted_expiry_date = aes_encrypt(data['expiry_date'], config.AES_KEY)

    card = CreditCard(
        customer_id=data['customer_id'],
        card_number=encrypted_card_number,
        cvv=encrypted_cvv,
        expiry_date=encrypted_expiry_date
    )
    db.session.add(card)
    db.session.commit()
    return jsonify({"message": "Card added successfully!"}), 201

@credit_card_bp.route('/<int:customer_id>', methods=['GET'])
def get_card(customer_id):
    card = CreditCard.query.filter_by(customer_id=customer_id).first()
    if card:
        return jsonify({
            "card_number": aes_decrypt(card.card_number, config.AES_KEY),
            "cvv": aes_decrypt(card.cvv, config.AES_KEY),
            "expiry_date": aes_decrypt(card.expiry_date, config.AES_KEY)
        }), 200
    return jsonify({"message": "Card not found"}), 404