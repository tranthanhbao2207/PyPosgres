import logging
import os
import sys
import time
import datetime as dt
import flask_sqlalchemy as f_sa

from flask import Flask


app = Flask(__name__)

POSTGRES_URL="127.0.0.1:54322"
POSTGRES_USER="postgres"
POSTGRES_DB="test"

class Config(object):
    DEBUG = True
    PASSWORD_HASH = 'talaai'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}@{url}/{db}'.format(user=POSTGRES_USER,url=POSTGRES_URL,db=POSTGRES_DB)


app.config.from_object(Config)
db = f_sa.SQLAlchemy(app)


@app.route('/')
def index():
    return 'hello'



if __name__ == "__main__":
       app.run(host='0.0.0.0', debug=True, port=4000)
