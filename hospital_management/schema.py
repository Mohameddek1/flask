from database import ma
from models import Patient, Doctor, Appointment

class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient

class DoctorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Doctor

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)
doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)