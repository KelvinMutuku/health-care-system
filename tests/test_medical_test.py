import unittest
import sqlite3 as sql
import database as db

class TestMedicalTestFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up a connection to a test database and create a cursor.
        Create a test table and insert sample data.
        """
        self.conn, self.c = db.connection()
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS medical_test_record (
                id TEXT PRIMARY KEY,
                test_name TEXT NOT NULL,
                patient_id TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                medical_lab_scientist_id TEXT,
                test_date_time TEXT NOT NULL,
                result_date_time TEXT,
                result_and_diagnosis TEXT,
                description TEXT,
                comments TEXT,
                cost INTEGER
            )
            """
        )
        self.sample_medical_test_data = [
            {
                "id": "MT-TEST-001",
                "test_name": "Blood Test",
                "patient_id": "P-001",
                "patient_name": "Test Patient 1",
                "doctor_id": "DR-001",
                "doctor_name": "Test Doctor 1",
                "medical_lab_scientist_id": "MLS-001",
                "test_date_time": "2024-01-15 10:00:00",
                "result_date_time": "2024-01-15 12:00:00",
                "result_and_diagnosis": "Normal",
                "description": "Routine blood test",
                "comments": "Fasting sample",
                "cost": 50
            },
            {
                "id": "MT-TEST-002",
                "test_name": "X-Ray",
                "patient_id": "P-002",
                "patient_name": "Test Patient 2",
                "doctor_id": "DR-002",
                "doctor_name": "Test Doctor 2",
                "medical_lab_scientist_id": "MLS-002",
                "test_date_time": "2024-01-16 14:00:00",
                "result_date_time": "2024-01-16 15:00:00",
                "result_and_diagnosis": "Fracture in left arm",
                "description": "X-ray of left arm",
                "comments": "Wear protective gear",
                "cost": 100
            }
        ]
        for test_data in self.sample_medical_test_data:
            placeholders = ", ".join(["?" for _ in test_data])
            columns = ", ".join(test_data.keys())
            sql = f"INSERT INTO medical_test_record ({columns}) VALUES ({placeholders})"
            self.c.execute(sql, tuple(test_data.values()))
        self.conn.commit()

    def tearDown(self):
        """
        Clean up after each test. Close the connection and
        delete the test table.
        """
        self.conn.close()
        self.conn = sql.connect('his.db')
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE IF EXISTS medical_test_record")
        self.conn.commit()
        self.conn.close()

    def test_verify_medical_test_id_exists(self):
        """
        Test that verify_medical_test_id returns True if the ID exists.
        """
        from medical_test import verify_medical_test_id
        self.assertTrue(verify_medical_test_id('MT-TEST-001'))

    def test_verify_medical_test_id_not_exists(self):
        """
        Test that verify_medical_test_id returns False if the ID doesn't exist.
        """
        from medical_test import verify_medical_test_id
        self.assertFalse(verify_medical_test_id('NON-EXISTENT-ID'))

if __name__ == '__main__':
    unittest.main()