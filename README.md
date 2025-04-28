#   Healthcare Information System

This is a Streamlit-based Healthcare Information System (HIS) designed to manage patient, doctor, health program, prescription, and medical test data. The system uses SQLite for data storage and provides a user-friendly interface for various administrative and clinical tasks.

##   Features

* **Patient Management:**
    * Add, update, delete, and search patient records.
    * View complete patient details, including personal information, contact details, and next of kin information.
* **Doctor Management:**
    * Add, update, delete, and search doctor records.
    * View doctor details, including specialization, qualification, and health program affiliation.
* **Health Program Management:**
    * Add, update, delete, and search health program records.
    * View health program details and a list of associated doctors.
* **Prescription Management:**
    * Add, update, delete, and view prescription records.
    * Search prescriptions by patient.
* **Medical Test Management:**
    * Add, update, delete, and view medical test records.
    * Search medical tests by patient.
* **User Authentication:**
    * Password-protected access to the system.
    * Edit mode protected by a separate password for data modification.
    * Doctor/Medical Lab Scientist access code for prescription and medical test management.

##   Modules

The system is organized into the following modules:

* `config.py`:  Contains configuration settings for database connection and user authentication.
* `database.py`: Handles database connection and table creation.
* `patient.py`:  Implements patient-related functionalities.
* `doctor.py`:   Implements doctor-related functionalities.
* `health_program.py`: Implements health program-related functionalities.
* `prescription.py`: Implements prescription-related functionalities.
* `medical_test.py`: Implements medical test-related functionalities.
* `hims_app.py`:  The main application file that integrates all the modules and provides the user interface.

##   Database

The system uses SQLite to store data in the following tables:

* `patient_record`: Stores patient information.
* `doctor_record`: Stores doctor information.
* `health_program_record`: Stores health program information.
* `prescription_record`: Stores prescription information.
* `medical_test_record`: Stores medical test information.

##   Setup

1.  **Installation:**
    * Ensure you have Python 3.x installed.
    * Install the required packages: `streamlit`, `pandas`, and `pysqlite3`.  You can install them using pip:
        ```bash
        pip install streamlit pandas pysqlite3
        ```
2.  **Configuration:**
    * Modify the `config.py` file to set your desired passwords and database name.
3.  **Running the Application:**
    * Execute the `hims_app.py` file using Streamlit:
        ```bash
        streamlit run hims_app.py
        ```

##   Security

* The system employs password protection to control access.
* An edit-mode password is required for modifying data.
* A separate access code is used for doctor/MLS prescription and test management.

##   API Usage (Patient API)

The system includes a Flask API to access patient information.

###   Running the API

1.  **Installation:**
    * Ensure you have Python 3.x installed.
    * Install the required packages: `Flask` and `pysqlite3`. You can install them using pip:
        ```bash
        pip install Flask pysqlite3
        ```
2.  **Running the API Server:**
    * Navigate to the directory containing `patient_api.py`.
    * Execute the script:
        ```bash
        python patient_api.py
        ```
    * The Flask development server will start, usually on `http://127.0.0.1:5000`.

###   API Endpoint

* `http://127.0.0.1:5000/patients/<patient_id>`:  Retrieves the details of the patient with the specified `patient_id`.

###   Example Usage

To get the details of the patient with ID "P-432921-250425", you would access the following URL in your browser or using a tool like `curl` or `httpie`: http://127.0.0.1:5000/patients/P-432921-250425

The API will return a JSON response containing the patient's information.

**Note:** The API server needs to be running separately from the Streamlit application.
**Prototype Demonstration Link:** https://drive.google.com/file/d/1liIdYRY8UGXUv69R7ms7EF49kN5O6i2F/view?usp=sharing
**Deployment Link:** https://kelvinmutuku-health-care-system-hims-app-uxukq2.streamlit.app/