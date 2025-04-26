import unittest
import sqlite3 as sql
import database as db

class TestHealthProgramFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up a connection to a test database and create a cursor.
        Create a test table and insert sample data.
        """
        self.conn, self.c = db.connection()
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS health_program_record (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                contact_number_1 TEXT NOT NULL,
                contact_number_2 TEXT,
                address TEXT NOT NULL,
                email_id TEXT
            )
            """
        )
        self.sample_health_program_data = [
            {
                "id": "HP-TEST-001",
                "name": "Cardiology Program",
                "description": "Program for heart-related conditions",
                "contact_number_1": "111-222-3333",
                "contact_number_2": None,
                "address": "Heart Center",
                "email_id": "cardio@program.com"
            },
            {
                "id": "HP-TEST-002",
                "name": "Pediatrics Program",
                "description": "Program for children's health",
                "contact_number_1": "444-555-6666",
                "contact_number_2": "777-888-9999",
                "address": "Children's Hospital",
                "email_id": "peds@program.com"
            }
        ]
        for program_data in self.sample_health_program_data:
            placeholders = ", ".join(["?" for _ in program_data])
            columns = ", ".join(program_data.keys())
            sql = f"INSERT INTO health_program_record ({columns}) VALUES ({placeholders})"
            self.c.execute(sql, tuple(program_data.values()))
        self.conn.commit()

    def tearDown(self):
        """
        Clean up after each test. Close the connection and
        delete the test table.
        """
        self.conn.close()
        self.conn = sql.connect('his.db')
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE IF EXISTS health_program_record")
        self.conn.commit()
        self.conn.close()

    def test_verify_health_program_id_exists(self):
        """
        Test that verify_health_program_id returns True if the ID exists.
        """
        from health_program import verify_health_program_id
        self.assertTrue(verify_health_program_id('HP-TEST-001'))

    def test_verify_health_program_id_not_exists(self):
        """
        Test that verify_health_program_id returns False if the ID doesn't exist.
        """
        from health_program import verify_health_program_id
        self.assertFalse(verify_health_program_id('NON-EXISTENT-ID'))

if __name__ == '__main__':
    unittest.main()