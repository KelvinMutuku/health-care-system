# Health Information System

## 📌 Features
- Register clients
- Enroll clients in health programs
- Search + view client profiles
- Secure API with JWT
- Deployed to Render

## 🧱 Stack
- Django + SQLite
- DRF (API)
- HTML/CSS3
- JWT Authentication

## 🚀 How to Run
```bash
git clone ...
cd health-care-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
🔒 API Auth
bash
Copy
Edit
POST /api/token/ { username, password }
🧪 Tests
bash
Copy
Edit
python manage.py test
yaml
Copy
Edit