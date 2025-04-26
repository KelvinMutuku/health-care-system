import unittest
import sqlite3 as sql
import database as db

class TestPrescriptionFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up a connection to a test database and create a cursor.
        Create a test table and insert sample data.
        """
        self.conn, self.c = db.connection()
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS prescription_record (
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                diagnosis TEXT,
                comments TEXT,
                medicine_1_name TEXT,
                medicine_1_dosage_description TEXT,
                medicine_2_name TEXT,
                medicine_2_dosage_description TEXT,
                medicine_3_name TEXT,
                medicine_3_dosage_description TEXT
            )
            """
        )
        self.sample_prescription_data = [
            {
                "id": "PR-TEST-001",
                "patient_id": "P-001",
                "patient_name": "Test Patient 1",
                "doctor_id": "DR-001",
                "doctor_name": "Test Doctor 1",
                "diagnosis": "Common Cold",
                "comments": "Rest and drink plenty of fluids",
                "medicine_1_name": "Paracetamol",
                "medicine_1_dosage_description": "500mg, twice a day",
                "medicine_2_name": None,
                "medicine_2_dosage_description": None,
                "medicine_3_name": None,
                "medicine_3_dosage_description": None
            },
            {
                "id": "PR-TEST-002",
                "patient_id": "P-002",
                "patient_name": "Test Patient 2",
                "doctor_id": "DR-002",
                "doctor_name": "Test Doctor 2",
                "diagnosis": "Flu",
                "comments": "Get vaccinated next year",
                "medicine_1_name": "Ibuprofen",
                "medicine_1_dosage_description": "200mg, thrice a day",
                "medicine_2_name": "Vitamin C",
                "medicine_2_dosage_description": "1000mg, once a day",
                "medicine_3_name": None,
                "medicine_3_dosage_description": None
            }
        ]
        for prescription_data in self.sample_prescription_data:
            placeholders = ", ".join(["?" for _ in prescription_data])
            columns = ", ".join(prescription_data.keys())
            sql = f"INSERT INTO prescription_record ({columns}) VALUES ({placeholders})"
            self.c.execute(sql, tuple(prescription_data.values()))
        self.conn.commit()

    def tearDown(self):
        """
        Clean up after each test. Close the connection and
        delete the test table.
        """
        self.conn.close()
        self.conn = sql.connect('his.db')
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE IF EXISTS prescription_record")
        self.conn.commit()
        self.conn.close()

    def test_verify_prescription_id_exists(self):
        """
        Test that verify_prescription_id returns True if the ID exists.
        """
        from prescription import verify_prescription_id
        self.assertTrue(verify_prescription_id('PR-TEST-001'))

    def test_verify_prescription_id_not_exists(self):
        """
        Test that verify_prescription_id returns False if the ID doesn't exist.
        """
        from prescription import verify_prescription_id
        self.assertFalse(verify_prescription_id('NON-EXISTENT-ID'))

if __name__ == '__main__':
    unittest.main()