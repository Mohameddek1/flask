from flask import Blueprint, request, jsonify
from models import Patient, Doctor, Appointment
from database import db
from schema import patient_schema, patients_schema

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(name=data['name'], age=data['age'], disease=data['disease'])
    db.session.add(new_patient)
    db.session.commit()
    return patient_schema.jsonify(new_patient)

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    all_patients = Patient.query.all()
    return patients_schema.jsonify(all_patients)