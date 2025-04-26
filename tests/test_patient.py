import unittest
from patient import calculate_age
from datetime import date

class TestPatientFunctions(unittest.TestCase):

    def test_calculate_age_basic(self):
        dob = date(1990, 1, 1)
        today = date(2024, 1, 1)
        self.assertEqual(calculate_age(dob), 34)

    def test_calculate_age_leap_year(self):
        dob = date(2000, 2, 29)  # Leap year
        today = date(2024, 3, 1)
        self.assertEqual(calculate_age(dob), 24)

    def test_calculate_age_birthday_not_yet(self):
        dob = date(1988, 12, 31)
        today = date(2024, 1, 15)
        self.assertEqual(calculate_age(dob), 36)

if __name__ == '__main__':
    unittest.main()