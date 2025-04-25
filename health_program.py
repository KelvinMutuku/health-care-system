import streamlit as st
from datetime import datetime
import database as db
import pandas as pd

# function to verify health_program id
def verify_health_program_id(health_program_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM health_program_record;
            """
        )
    for id in c.fetchall():
        if id[0] == health_program_id:
            verify = True
            break
    conn.close()
    return verify

# function to show the details of health_program(s) given in a list (provided as a parameter)
def show_health_program_details(list_of_health_programs):
    health_program_titles = ['health_program ID', 'health_program name', 'Description', 'Contact number',
                     'Alternate contact number', 'Address', 'Email ID']
    if len(list_of_health_programs) == 0:
        st.warning('No data to show')
    elif len(list_of_health_programs) == 1:
        health_program_details = [x for x in list_of_health_programs[0]]
        series = pd.Series(data = health_program_details, index = health_program_titles)
        st.write(series)
    else:
        health_program_details = []
        for health_program in list_of_health_programs:
            health_program_details.append([x for x in health_program])
        df = pd.DataFrame(data = health_program_details, columns = health_program_titles)
        st.write(df)

# function to generate unique health_program id using current date and time
def generate_health_program_id():
    id_1 = datetime.now().strftime('%S%M%H')
    id_2 = datetime.now().strftime('%Y%m%d')[2:]
    id = f'D-{id_1}-{id_2}'
    return id

# function to show the doctor id and name of doctor(s) given in a list (provided as a parameter)
def show_list_of_doctors(list_of_doctors):
    doctor_titles = ['Doctor ID', 'Name']
    if len(list_of_doctors) == 0:
        st.warning('No data to show')
    else:
        doctor_details = []
        for doctor in list_of_doctors:
            doctor_details.append([x for x in doctor])
        df = pd.DataFrame(data = doctor_details, columns = doctor_titles)
        st.write(df)

# function to fetch health_program name from the database for the given health_program id
def get_health_program_name(dept_id):
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT name
            FROM health_program_record
            WHERE id = :id;
            """,
            { 'id': dept_id }
        )
    return c.fetchone()[0]

# class containing all the fields and methods required to work with the health_programs' table in the database
class Health_program:

    def __init__(self):
        self.name = str()
        self.id = str()
        self.description = str()
        self.contact_number_1 = str()
        self.contact_number_2 = str()
        self.address = str()
        self.email_id = str()

    # method to add a new health_program record to the database
    def add_health_program(self):
        st.write('Enter health_program details:')
        self.name = st.text_input('health_program name')
        self.description = st.text_area('Description')
        self.contact_number_1 = st.text_input('Contact number')
        contact_number_2 = st.text_input('Alternate contact number (optional)')
        self.contact_number_2 = (lambda phone : None if phone == '' else phone)(contact_number_2)
        self.address = st.text_area('Address')
        self.email_id = st.text_input('Email ID')
        self.id = generate_health_program_id()
        save = st.button('Save')

        # executing SQLite statements to save the new health_program record to the database
        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO health_program_record
                    (
                        id, name, description, contact_number_1, contact_number_2,
                        address, email_id
                    )
                    VALUES (
                        :id, :name, :desc, :phone_1, :phone_2, :address, :email_id
                    );
                    """,
                    {
                        'id': self.id, 'name': self.name, 'desc': self.description,
                        'phone_1': self.contact_number_1,
                        'phone_2': self.contact_number_2, 'address': self.address,
                        'email_id': self.email_id
                    }
                )
            st.success('Health_program details saved successfully.')
            st.write('The Health_program ID is: ', self.id)
            conn.close()

    # method to update an existing health_program record in the database
    def update_health_program(self):
        id = st.text_input('Enter Health_program ID of the health_program to be updated')
        if id == '':
            st.empty()
        elif not verify_health_program_id(id):
            st.error('Invalid Health_program ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the health_program before updating
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM health_program_record
                    WHERE id = :id;
                    """,
                    { 'id': id }
                )
                st.write('Here are the current details of the health_program:')
                show_health_program_details(c.fetchall())

            st.write('Enter new details of the health_program:')
            self.description = st.text_area('Description')
            self.contact_number_1 = st.text_input('Contact number')
            contact_number_2 = st.text_input('Alternate contact number (optional)')
            self.contact_number_2 = (lambda phone : None if phone == '' else phone)(contact_number_2)
            self.address = st.text_area('Address')
            self.email_id = st.text_input('Email ID')
            update = st.button('Update')

            # executing SQLite statements to update this health_program's record in the database
            if update:
                with conn:
                    c.execute(
                        """
                        UPDATE health_program_record
                        SET description = :desc,
                        contact_number_1 = :phone_1, contact_number_2 = :phone_2,
                        address = :address, email_id = :email_id
                        WHERE id = :id;
                        """,
                        {
                            'id': id, 'desc': self.description,
                            'phone_1': self.contact_number_1,
                            'phone_2': self.contact_number_2,
                            'address': self.address, 'email_id': self.email_id
                        }
                    )
                st.success('Health_program details updated successfully.')
                conn.close()

    # method to delete an existing health_program record from the database
    def delete_health_program(self):
        id = st.text_input('Enter Health_program ID of the health_program to be deleted')
        if id == '':
            st.empty()
        elif not verify_health_program_id(id):
            st.error('Invalid Health_program ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            # shows the current details of the health_program before deletion
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM health_program_record
                    WHERE id = :id;
                    """,
                    { 'id': id }
                )
                st.write('Here are the details of the health_program to be deleted:')
                show_health_program_details(c.fetchall())

                confirm = st.checkbox('Check this box to confirm deletion')
                if confirm:
                    delete = st.button('Delete')

                    # executing SQLite statements to delete this health_program's record from the database
                    if delete:
                        c.execute(
                            """
                            DELETE FROM health_program_record
                            WHERE id = :id;
                            """,
                            { 'id': id }
                        )
                        st.success('Health_program details deleted successfully.')
            conn.close()

    # method to show the complete health_program record
    def show_all_health_programs(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM health_program_record;
                """
            )
            show_health_program_details(c.fetchall())
        conn.close()

    # method to search and show a particular health_program's details in the database using health_program id
    def search_health_program(self):
        id = st.text_input('Enter Health_program ID of the health_program to be searched')
        if id == '':
            st.empty()
        elif not verify_health_program_id(id):
            st.error('Invalid Health_program ID')
        else:
            st.success('Verified')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM health_program_record
                    WHERE id = :id;
                    """,
                    { 'id': id }
                )
                st.write('Here are the details of the health_program you searched for:')
                show_health_program_details(c.fetchall())
            conn.close()

    # method to show the list of doctors working in a particular health_program (using health_program id)
    def list_dept_doctors(self):
        dept_id = st.text_input('Enter Health_program ID to get a list of doctors working in that health_program')
        if dept_id == '':
            st.empty()
        elif not verify_health_program_id(dept_id):
            st.error('Invalid health_program ID')
        else:
            st.success('Verified')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT id, name
                    FROM doctor_record
                    WHERE health_program_id = :dept_id;
                    """,
                    { 'dept_id': dept_id }
                )
                st.write('Here is the list of doctors working in the', get_health_program_name(dept_id), 'health_program:')
                show_list_of_doctors(c.fetchall())
            conn.close()