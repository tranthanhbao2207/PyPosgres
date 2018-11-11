#!/usr/bin/env bash
FLASK_APP=app/app.py
flask db init
flask db migrate -m " table"
flask db upgrade
