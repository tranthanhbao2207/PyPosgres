#!/usr/bin/env bash
 psql -U postgres -p 54322 -h 127.0.0.1 -c "DROP DATABASE if exists atlas_test; CREATE DATABASE test_bao";
 FLASK_APP=app.py flask db init;
 FLASK_APP=app.py flask db migrate -m " table";
 FLASK_APP=app.py flask db upgrade;
