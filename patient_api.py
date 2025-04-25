from flask import Flask, jsonify
import database as db

app = Flask(__name__)

@app.route('/patients/<string:patient_id>', methods=['GET'])
def get_patient_profile(patient_id):
    conn, c = db.connection()
    with conn:
        c.execute("""
            SELECT * FROM patient_record WHERE id = :id
        """, {'id': patient_id})
        patient = c.fetchone()
    conn.close()

    if patient:
        patient_data = dict(zip(['id', 'name', 'age', 'gender', 'date_of_birth', 'blood_group', 'contact_number_1', 'contact_number_2', 'weight', 'height', 'address', 'city', 'state', 'pin_code', "next_of_kin_name", "next_of_kin_relation_to_patient", "next_of_kin_contact_number", 'email_id', 'date_of_registration', 'time_of_registration'], patient))

        # Get enrolled programs (using the function from earlier)
        import enrollment
        enrolled_programs = enrollment.get_programs_for_patient(patient_id)
        patient_data['enrolled_programs'] = enrolled_programs

        return jsonify(patient_data)
    else:
        return jsonify({'error': 'Patient not found'}), 404  # Not Found status code

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask development server