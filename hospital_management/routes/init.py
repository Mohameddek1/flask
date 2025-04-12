from flask import Blueprint
from routes.patients_route import patient_bp
from routes.doctors_routes import doctor_bp
from routes.appointment_routes import appointment_bp

def register_blueprint(app):
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(appointment_bp)
    