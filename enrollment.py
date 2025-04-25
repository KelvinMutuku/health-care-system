import database as db
import datetime


def enroll_patient_in_program(patient_id, health_program_id):
    conn, c = db.connection()
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    with conn:
        try:
            c.execute(
                """
                INSERT INTO patient_program_enrollment
                (patient_id, health_program_id, enrollment_date)
                VALUES (:patient_id, :health_program_id, :enrollment_date);
                """,
                {'patient_id': patient_id, 'health_program_id': health_program_id, 'enrollment_date': now}
            )
            return True
        except db.sql.IntegrityError:
            return False  # Patient already enrolled


def get_programs_for_patient(patient_id):
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT hr.name, hr.description, hr.id
            FROM patient_program_enrollment ppe
            JOIN health_program_record hr ON ppe.health_program_id = hr.id
            WHERE ppe.patient_id = :patient_id;
            """,
            {'patient_id': patient_id}
        )
        return c.fetchall()  # Returns a list of tuples