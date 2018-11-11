FLASK_APP=app/app.py
flask db migrate -m "users table"
flask db upgrade
