import unittest
import sqlite3 as sql
import database as db
import sys
import os

class TestDoctorFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up a connection to a test database and create a cursor.
        Create a test table and insert sample data.
        """
        self.conn, self.c = db.connection()
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS doctor_record (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                health_program_id TEXT,
                health_program_name TEXT,
                contact_number_1 TEXT NOT NULL,
                contact_number_2 TEXT,
                email_id TEXT,
                qualification TEXT,
                specialisation TEXT,
                years_of_experience INTEGER,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                pin_code TEXT NOT NULL
            )
            """
        )
        self.sample_doctor_data = [
            {
                "id": "DR-TEST-001",
                "name": "Test Doctor 1",
                "age": 35,
                "gender": "Male",
                "date_of_birth": "10-03-1989",
                "blood_group": "A+",
                "health_program_id": "HP-001",
                "health_program_name": "Cardiology Program",
                "contact_number_1": "123-456-7890",
                "contact_number_2": None,
                "email_id": "test1@doctor.com",
                "qualification": "MD",
                "specialisation": "Cardiology",
                "years_of_experience": 8,
                "address": "1st Street",
                "city": "Test City",
                "state": "Test State",
                "pin_code": "12345"
            },
            {
                "id": "DR-TEST-002",
                "name": "Test Doctor 2",
                "age": 42,
                "gender": "Female",
                "date_of_birth": "20-05-1982",
                "blood_group": "B-",
                "health_program_id": "HP-002",
                "health_program_name": "Pediatrics Program",
                "contact_number_1": "098-765-4321",
                "contact_number_2": "111-222-3333",
                "email_id": "test2@doctor.com",
                "qualification": "MBBS",
                "specialisation": "Pediatrics",
                "years_of_experience": 15,
                "address": "2nd Avenue",
                "city": "Another City",
                "state": "Another State",
                "pin_code": "54321"
            }
        ]
        for doctor_data in self.sample_doctor_data:
            placeholders = ", ".join(["?" for _ in doctor_data])
            columns = ", ".join(doctor_data.keys())
            sql = f"INSERT INTO doctor_record ({columns}) VALUES ({placeholders})"
            self.c.execute(sql, tuple(doctor_data.values()))
        self.conn.commit()

    def tearDown(self):
        """
        Clean up after each test. Close the connection and
        delete the test table to ensure a clean slate for next test.
        """
        self.conn.close()
        self.conn = sql.connect('his.db')
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE IF EXISTS doctor_record")
        self.conn.commit()
        self.conn.close()

    def test_verify_doctor_id_exists(self):
        """
        Test that verify_doctor_id returns True if the ID exists.
        """
        from doctor import verify_doctor_id  # Import here to avoid global scope issues
        self.assertTrue(verify_doctor_id('DR-TEST-001'))

    def test_verify_doctor_id_not_exists(self):
        """
        Test that verify_doctor_id returns False if the ID doesn't exist.
        """
        from doctor import verify_doctor_id
        self.assertFalse(verify_doctor_id('NON-EXISTENT-ID'))

if __name__ == '__main__':
    unittest.main()