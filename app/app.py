from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import logging
import os
import sys
import time
import datetime as dt
import flask_sqlalchemy as f_sa
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import werkzeug.exceptions as w_exc
from flask_login import (
    current_user,
    confirm_login,
    LoginManager,
    logout_user,
    login_required,
    login_user,
)
from flask_migrate import Migrate
from flask import (
    Flask,
    jsonify,
    redirect,
    request,
)
import ujson
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import flask_sqlalchemy as f_sa


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
migrate = Migrate(app, db)
login = LoginManager(app)



## models.py

class MinBase(object):
    f_changed = db.Column(db.DateTime, nullable=True, onupdate=sa.func.now())
    deleted   = db.Column(db.Boolean, nullable=False, default=False)


class User(MinBase, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Customer(MinBase, db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
            return '<Cust {}>'.format(self.name)


## utils


def to_dict(row):
        dic = {}
        for column in row.__table__.columns:
            dic[column.name] = str(getattr(row, column.name))
        return dic

## common sql
def insert_data(cls, data):
    statement = User.__table__.insert().values(**data)
    try:
        res = db.session.execute(statement)
        return res.inserted_primary_key
    except ValueError:
        db.session.rollback()
        raise ValueError('Failed to insert {cls} - {data}'.format(
            cls=cls,data=data
        ))

def get_data(CLS, id=None):
    query = db.session.query(
        CLS
    ).\
    filter(
        CLS.deleted == 'F',
    )

    query = query.filter(CLS.id == id).first() if id else query.all()

    res = to_dict(query) if id else [
        to_dict(row)
        for row in query
    ]
    return res



def update_data(CLS,id , data):
    pass


## API
@app.route("/login2", methods=["GET", "POST"])
def login2():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')

    if not username:
        raise w_exc.BadRequest(' username ?')
    if not password:
        raise w_exc.BadRequest(' password ?')

    user = db.session.query(User). \
        filter(User.username == username). \
        first()

    if user and check_password_hash(user.password, password):
        print('ss')
        login_user(user,remember=False)
        confirm_login()
        return 200
    else:
        raise w_exc.BadRequest('not username or password')



## TODO: Login required
@app.route('/customer', methods=["GET", "POST","PUT"])
@app.route('/customer/<id>', methods=["GET", "POST","PUT"])
def customer(id=None):
    if request.method != 'GET':
        data = ujson.loads(request.data)

        if request.method != 'POST':
            if id is None:
                raise w_exc.BadRequest(' Require customer id')

            cust_to_update = db.session.query(User).filter(User.id == id).first()

            if cust_to_update is None:
                raise w_exc.BadRequest(' invalid id !')

        values = {
            k : data[k] if k != 'password' else generate_password_hash(data[k])
            for k in data
        }

        customer = Customer(**values)

        try:
            if request.method == 'POST':
                db.session.add(customer)
            else:
                db.session.query(Customer.id == id ).update(values)
            db.session.commit()
            new_id = customer.id
            return '{action} Customer - {id}'.format(
                    action='inserted' if request.method == 'POST' else 'updated',
                    id=new_id,
                ) ,200
        except ValueError:
            db.session.rollback()
            raise ValueError('Failed to insert User - {data}'.format(
                data=data
            ))

    res = get_data(Customer, id)
    return jsonify(res), 200


@app.route('/zuser', methods=["GET", "POST","PUT"])
@app.route('/zuser/<id>', methods=["GET", "POST","PUT"])
def zuser(id=None):
    if request.method != 'GET':
        data = ujson.loads(request.data)

        if request.method == 'POST':
            existed = db.session.query(User).filter(User.username== data['username']).first()
            if existed is not None:
                raise w_exc.BadRequest(' existed username !')

            if 'username' not in data or 'password' not in data:
                raise w_exc.BadRequest(' username or password ?')
        else:
            if not id:
                raise w_exc.BadRequest('Update requie user id ')

            user_to_update = db.session.query(User).filter(User.id == id).first()

            if user_to_update is None:
                raise w_exc.BadRequest('invalid requie user id ')

            if user_to_update.username == data['username']:
                raise w_exc.BadRequest(' exist usernam !')

        values = {
            k : data[k] if k != 'password' else generate_password_hash(data[k])
            for k in data
        }
        user = User(**values)
        try:
            if request.method == 'POST':
                db.session.add(user)
            else:
                db.session.query(User.id == id ).update(values)
            db.session.commit()
            new_id = user.id
            return '{action} User - {id}'.format(
                    action='inserted' if request.method == 'POST' else 'updated',
                    id=new_id,
                ) ,200
        except ValueError:
            db.session.rollback()
            raise ValueError('Failed to insert User - {data}'.format(
                data=data
            ))

    res = get_data(User, id)

    return jsonify(res),200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4100)
