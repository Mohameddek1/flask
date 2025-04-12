from flask import Blueprint, request, jsonify
from models import Doctor
from database import db
from schema import doctor_schema, doctors_schema

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    new_doctor = Doctor(name=data['name'], speciality=data['speciality'])
    db.session.add(new_doctor)
    db.session.commit()
    return doctor_schema.jsonify(new_doctor)

@doctor_bp.route('/doctors', methods=['GET'])
def get_doctors():
    all_doctors = Doctor.query.all()
    return doctors_schema.jsonify(all_doctors)