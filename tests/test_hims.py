import unittest
from datetime import date
import database as db
import doctor
import health_program
import patient
import prescription
import medical_test

# --- Helper function to insert data ---
def insert_test_data(cursor, table_name, data):
    """Inserts data into the specified table."""
    placeholders = ", ".join(["?" for _ in data[0]])
    columns = ", ".join(data[0].keys())
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    for row in data:
        values = tuple(row.values())
        cursor.execute(sql, values)

class TestHIMS(unittest.TestCase):

    def setUp(self):
        """Set up a connection to a test database and create tables."""
        self.conn, self.c = db.connection()
        db.db_init()  # Initialize the database tables

        # --- Insert sample data ---
        self.sample_patient_data = [{
            "id": "P-TEST-001",
            "name": "Test Patient",
            "age": 30,
            "gender": "Male",
            "date_of_birth": "01-01-1994",
            "blood_group": "A+",
            "contact_number_1": "123-456-7890",
            "contact_number_2": None,
            "weight": 70,
            "height": 175,
            "address": "Test Address",
            "city": "Test City",
            "state": "Test State",
            "pin_code": "12345",
            "next_of_kin_name": "Test Kin",
            "next_of_kin_relation_to_patient": "Brother",
            "next_of_kin_contact_number": "098-765-4321",
            "email_id": "test@email.com",
            "date_of_registration": "2024-01-01",
            "time_of_registration": "10:00:00"
        }]
        insert_test_data(self.c, "patient_record", self.sample_patient_data)

        self.sample_doctor_data = [{
            "id": "DR-TEST-001",
            "name": "Test Doctor",
            "age": 40,
            "gender": "Female",
            "date_of_birth": "15-08-1984",
            "blood_group": "O+",
            "health_program_id": "HP-TEST-001",
            "health_program_name": "Test Program",
            "contact_number_1": "0722-111222",
            "contact_number_2": "0733-111222",
            "email_id": "aisha.mwangi@doctors.co.ke",
            "qualification": "MD, Cardiology",
            "specialisation": "Cardiology",
            "years_of_experience": 10,
            "address": "9 Doctor Plaza, Nairobi",
            "city": "Nairobi",
            "state": "Nairobi",
            "pin_code": "00100",
        }]
        insert_test_data(self.c, "doctor_record", self.sample_doctor_data)

        self.sample_health_program_data = [{
            "id": "HP-TEST-001",
            "name": "Test Program",
            "description": "Test Description",
            "contact_number_1": "020-123-4567",
            "contact_number_2": "0722-123456",
            "address": "12 Heart Street, Nairobi",
            "email_id": "cardio@health.co.ke",
        }]
        insert_test_data(self.c, "health_program_record", self.sample_health_program_data)

        self.sample_prescription_data = [{
            "id": "PR-TEST-001",
            "patient_id": "P-TEST-001",
            "patient_name": "Test Patient",
            "doctor_id": "DR-TEST-001",
            "doctor_name": "Test Doctor",
            "diagnosis": "Test Diagnosis",
            "comments": "Test Comments",
            "medicine_1_name": "Test Medicine 1",
            "medicine_1_dosage_description": "Test Dosage 1",
            "medicine_2_name": None,
            "medicine_2_dosage_description": None,
            "medicine_3_name": None,
            "medicine_3_dosage_description": None,
        }]
        insert_test_data(self.c, "prescription_record", self.sample_prescription_data)

        self.sample_medical_test_data = [{
            "id": "MT-TEST-001",
            "test_name": "Test ECG",
            "patient_id": "P-TEST-001",
            "patient_name": "Test Patient",
            "doctor_id": "DR-TEST-001",
            "doctor_name": "Test Doctor",
            "medical_lab_scientist_id": "MLS-001",
            "test_date_time": "2024-01-02 09:00:00",
            "result_date_time": "2024-01-02 10:00:00",
            "result_and_diagnosis": "Normal",
            "description": "Test ECG Description",
            "comments": "Test ECG Comments",
            "cost": 2500,
        }]
        insert_test_data(self.c, "medical_test_record", self.sample_medical_test_data)
        self.conn.commit()

    def tearDown(self):
        """Clean up after each test by closing the connection and optionally deleting data."""
        self.conn.close()
        # --- OPTIONAL:  Clear data if needed ---
        # self.conn, self.c = db.connection()
        # self.c.execute("DELETE FROM patient_record")
        # self.c.execute("DELETE FROM doctor_record")
        # self.c.execute("DELETE FROM health_program_record")
        # self.c.execute("DELETE FROM prescription_record")
        # self.c.execute("DELETE FROM medical_test_record")
        # self.conn.commit()
        # self.conn.close()

    def test_verify_patient_id_exists(self):
        self.assertTrue(patient.verify_patient_id("P-TEST-001"))

    def test_verify_patient_id_not_exists(self):
        self.assertFalse(patient.verify_patient_id("NON-EXISTENT-ID"))

    def test_generate_patient_id(self):
        reg_date = "2024-01-10"
        reg_time = "14:30:15"
        expected_id_parts = ["P", "153014", "10012024"]
        generated_id = patient.generate_patient_id(reg_date, reg_time)
        for part in expected_id_parts:
            self.assertTrue(part in generated_id)

    def test_calculate_age(self):
        dob = date(1994, 1, 1)
        today = date(2024, 1, 1)
        self.assertEqual(patient.calculate_age(dob), 30)

    def test_verify_doctor_id_exists(self):
        self.assertTrue(doctor.verify_doctor_id("DR-TEST-001"))

    def test_verify_doctor_id_not_exists(self):
        self.assertFalse(doctor.verify_doctor_id("NON-EXISTENT-ID"))

    def test_verify_health_program_id_exists(self):
        self.assertTrue(health_program.verify_health_program_id("HP-TEST-001"))

    def test_verify_health_program_id_not_exists(self):
        self.assertFalse(health_program.verify_health_program_id("NON-EXISTENT-ID"))

    def test_verify_prescription_id_exists(self):
        self.assertTrue(prescription.verify_prescription_id("PR-TEST-001"))

    def test_verify_prescription_id_not_exists(self):
        self.assertFalse(prescription.verify_prescription_id("NON-EXISTENT-ID"))

    def test_verify_medical_test_id_exists(self):
        self.assertTrue(medical_test.verify_medical_test_id("MT-TEST-001"))

    def test_verify_medical_test_id_not_exists(self):
        self.assertFalse(medical_test.verify_medical_test_id("NON-EXISTENT-ID"))

if __name__ == '__main__':
    unittest.main()