import streamlit as st
import database as db
from patient import Patient
from health_program import Health_program
from doctor import Doctor
from prescription import Prescription
from medical_test import Medical_Test
import enrollment
import config
import sqlite3 as sql

# function to verify edit mode password
def verify_edit_mode_password():
    edit_mode_password = st.sidebar.text_input('Enter edit mode password', type = 'password')
    if edit_mode_password == config.edit_mode_password:
        st.sidebar.success('Verified')
        return True
    elif edit_mode_password == '':
        st.empty()
    else:
        st.sidebar.error('Invalid edit mode password')
        return False

# function to verify doctor/medical lab scientist access code
def verify_dr_mls_access_code():
    dr_mls_access_code = st.sidebar.text_input('Enter doctor/medical lab scientist access code', type = 'password')
    if dr_mls_access_code == config.dr_mls_access_code:
        st.sidebar.success('Verified')
        return True
    elif dr_mls_access_code == '':
        st.empty()
    else:
        st.sidebar.error('Invalid access code')
        return False

# function to perform various operations of the patient module (according to user's selection)
def patients():
    st.header('PATIENTS')
    option_list = ['', 'Add patient', 'Update patient', 'Delete patient',
                   'Show complete patient record', 'Search patient', "Enroll Patient in Health Program"]  # Add the new option
    option = st.sidebar.selectbox('Select function', option_list)
    p = Patient()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader('ADD PATIENT')
            p.add_patient()
        elif option == option_list[2]:
            st.subheader('UPDATE PATIENT')
            p.update_patient()
        elif option == option_list[3]:
            st.subheader('DELETE PATIENT')
            try:
                p.delete_patient()
            except sql.IntegrityError:  # handles foreign key constraint failure issue (due to integrity error)
                st.error('This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE PATIENT RECORD')
        p.show_all_patients()
    elif option == option_list[5]:
        st.subheader('SEARCH PATIENT')
        p.search_patient()
    elif option == option_list[6]:  # New enrollment option
        st.subheader("Enroll Patient in Program")
        # Get lists of patients and programs for selection
        conn, c = db.connection()
        with conn:
            c.execute("SELECT id, name FROM patient_record")
            patients = c.fetchall()
            c.execute("SELECT id, name FROM health_program_record")
            programs = c.fetchall()
        conn.close()
        patient_id = st.selectbox("Select Patient", [p[0] for p in patients],
                                     format_func=lambda x: f"{x} - {next(p[1] for p in patients if p[0] == x)}")
        program_ids = st.multiselect("Select Health Programs", [prog[0] for prog in programs],
                                      format_func=lambda x: f"{x} - {next(prog[1] for prog in programs if prog[0] == x)}")
        if st.button("Enroll"):
            for prog_id in program_ids:
                if enrollment.enroll_patient_in_program(patient_id, prog_id):
                    st.success(f"Enrolled patient {patient_id} in program {prog_id}")
                else:
                    st.warning(f"Patient {patient_id} already enrolled in program {prog_id}")
# function to perform various operations of the doctor module (according to user's selection)
def doctors():
    st.header('DOCTORS')
    option_list = ['', 'Add doctor', 'Update doctor', 'Delete doctor', 'Show complete doctor record', 'Search doctor']
    option = st.sidebar.selectbox('Select function', option_list)
    dr = Doctor()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader('ADD DOCTOR')
            dr.add_doctor()
        elif option == option_list[2]:
            st.subheader('UPDATE DOCTOR')
            dr.update_doctor()
        elif option == option_list[3]:
            st.subheader('DELETE DOCTOR')
            try:
                dr.delete_doctor()
            except sql.IntegrityError:      # handles foreign key constraint failure issue (due to integrity error)
                st.error('This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE DOCTOR RECORD')
        dr.show_all_doctors()
    elif option == option_list[5]:
        st.subheader('SEARCH DOCTOR')
        dr.search_doctor()

# function to perform various operations of the prescription module (according to user's selection)
def prescriptions():
    st.header('PRESCRIPTIONS')
    option_list = ['', 'Add prescription', 'Update prescription', 'Delete prescription', 'Show prescriptions of a particular patient']
    option = st.sidebar.selectbox('Select function', option_list)
    m = Prescription()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_dr_mls_access_code():
        if option == option_list[1]:
            st.subheader('ADD PRESCRIPTION')
            m.add_prescription()
        elif option == option_list[2]:
            st.subheader('UPDATE PRESCRIPTION')
            m.update_prescription()
        elif option == option_list[3]:
            st.subheader('DELETE PRESCRIPTION')
            m.delete_prescription()
    elif option == option_list[4]:
        st.subheader('PRESCRIPTIONS OF A PARTICULAR PATIENT')
        m.prescriptions_by_patient()

# function to perform various operations of the medical_test module (according to user's selection)
def medical_tests():
    st.header('MEDICAL TESTS')
    option_list = ['', 'Add medical test', 'Update medical test', 'Delete medical test', 'Show medical tests of a particular patient']
    option = st.sidebar.selectbox('Select function', option_list)
    t = Medical_Test()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_dr_mls_access_code():
        if option == option_list[1]:
            st.subheader('ADD MEDICAL TEST')
            t.add_medical_test()
        elif option == option_list[2]:
            st.subheader('UPDATE MEDICAL TEST')
            t.update_medical_test()
        elif option == option_list[3]:
            st.subheader('DELETE MEDICAL TEST')
            t.delete_medical_test()
    elif option == option_list[4]:
        st.subheader('MEDICAL TESTS OF A PARTICULAR PATIENT')
        t.medical_tests_by_patient()

# function to perform various operations of the health_program module (according to user's selection)
def health_programs():
    st.header('HEALTH PROGRAMS')
    option_list = ['', 'Add health program', 'Update health program', 'Delete health program', 'Show complete health program record', 'Search health program', 'Show doctors of a particular health program']
    option = st.sidebar.selectbox('Select function', option_list)
    d = Health_program()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader('ADD HEALTH PROGRAM')
            d.add_health_program()
        elif option == option_list[2]:
            st.subheader('UPDATE HEALTH PROGRAM')
            d.update_health_program()
        elif option == option_list[3]:
            st.subheader('DELETE HEALTH PROGRAM')
            try:
                d.delete_health_program()
            except sql.IntegrityError:      # handles foreign key constraint failure issue (due to integrity error)
                st.error('This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE HEALTH PROGRAM RECORD')
        d.show_all_health_programs()
    elif option == option_list[5]:
        st.subheader('SEARCH HEALTH PROGRAM')
        d.search_health_program()
    elif option == option_list[6]:
        st.subheader('DOCTORS OF A PARTICULAR HEALTH PROGRAM')
        d.list_hlthpg_doctors()

# function to implement and initialise home/main menu on successful user authentication
def home():
    db.db_init()        # establishes connection to the database and create tables (if they don't exist yet)
    option = st.sidebar.selectbox('Select module', ['', 'Patients', 'Doctors', 'Prescriptions', 'Medical Tests', 'Health Programs'])
    if option == 'Patients':
        patients()
    elif option == 'Doctors':
        doctors()
    elif option == 'Prescriptions':
        prescriptions()
    elif option == 'Medical Tests':
        medical_tests()
    elif option == 'Health Programs':
        health_programs()

st.title('HEALTHCARE INFORMATION SYSTEM')
password = st.sidebar.text_input('Enter password', type = 'password')       # user password authentication
if password == config.password:
    st.sidebar.success('Verified')
    home()
elif password == '':
    st.empty()
else:
    st.sidebar.error('Invalid password')