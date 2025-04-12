from flask import Blueprint, request, jsonify
from models import Appointment
from database import db
from schema import appointment_schema, appointments_schema

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    new_appointment = Appointment(patient_id=data['patient_id'], doctor_id=data['doctor_id'])
    db.session.add(new_appointment)
    db.session.commit()
    return appointment_schema.jsonify(new_appointment)

@appointment_bp.route('/appointments', methods=['GET'])
def get_appointments():
    all_appointments = Appointment.query.all()
    return appointments_schema.jsonify(all_appointments)