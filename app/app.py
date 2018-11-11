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
    session,
)
import ujson
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import flask_sqlalchemy as f_sa


app = Flask(__name__)

POSTGRES_URL = "127.0.0.1:54322"
POSTGRES_USER = "postgres"
POSTGRES_DB = "test"


class Config(object):
    DEBUG = True
    PASSWORD_HASH = 'talaai'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}@{url}/{db}'.format(
        user=POSTGRES_USER, url=POSTGRES_URL, db=POSTGRES_DB)
    SECRET_KEY = 'asd'


app.config.from_object(Config)
db = f_sa.SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


# models.py

class MinBase(object):
    f_changed = db.Column(db.DateTime, nullable=True, onupdate=sa.func.now())
    deleted = db.Column(db.Boolean, nullable=False, default=False)


class User(MinBase, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    # for flask-login

    def is_active(self):
        return True

    def is_authenticated(self):
        print('auth', self)
        return current_user.id == self.id

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_auth_token(self):
        pass


class Customer(MinBase, db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return '<Cust {}>'.format(self.name)

# utils


def to_dict(row):
    # simple result to dict
    dic = {}
    for column in row.__table__.columns:
        dic[column.name] = str(getattr(row, column.name))
    return dic


class attrdict(dict):
    def __getattr__(self, k):
        return self[k]

    def __settattribute(self, k, v):
        self[k] = v

# common sql


def insert_data(CLS, data):
    # statement = CLS.__table__.insert().values(**data) -- this didnt works . weird !
    try:
        db.session.add(data)
        db.session.commit()
        new_id = data.id
        return get_data(CLS, new_id)
    except ValueError:
        db.session.rollback()
        raise ValueError('Failed to insert User - {data}'.format(
            data=data
        ))


def update_data(CLS, id, values):
    try:
        db.session.query(CLS.id == id).update(values)
        db.session.commit()
        return get_data(CLS, id)
    except ValueError:
        db.session.rollback()
        raise ValueError('Failed to insert User - {data}'.format(
            data=values
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


# security
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
        filter(sa.or_(User.email == username, User.username == username), User.deleted == 'F'). \
        first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        confirm_login()
        return 'Login successfully !', 200
    else:
        raise w_exc.BadRequest('not username or password')


@app.route("/logout2")
@login_required
def logout():
    session["__invalidate__"] = True
    logout_user()
    return 'Logout successfully ', 200
    # redirect somewhere ?


@login_manager.user_loader
def load_user(userid):
    user = get_data(User, userid)
    if not zuser:
        return None
    user = attrdict(**user)
    user.is_authenticated = lambda: True
    user.is_anonymous = lambda: False
    user.roles = []
    user.rights = []  # rights to update/insert entities (customer,user,...) ?
    return user

# api.py


@app.route('/customer', methods=["GET", "POST"])
@app.route('/customer/<id>', methods=["GET", "PUT"])
@login_required
def customer(id=None):
    if request.method != 'GET':
        data = ujson.loads(request.data)

        if request.method != 'POST':
            if id is None:
                raise w_exc.BadRequest(' Require customer id')

            cust_to_update = db.session.query(
                User).filter(User.id == id).first()

            if cust_to_update is None:
                raise w_exc.BadRequest(' invalid id !')

        values = {
            k: data[k]
            for k in data
        }

        customer = Customer(**values)

        res = dict()
        if request.method == 'POST':
            res = insert_data(Customer, customer)
            return jsonify(res), 200
        else:
            res = update_data(Customer, id, values)

        if hasattr(res, 'id'):
            return jsonify(res), 200
        else:
            # TODO: custom error msg
            w_exc.BadRequest(' cound not insert')

    res = get_data(Customer, id)
    return jsonify(res), 200


@app.route('/zuser', methods=["GET", "POST"])
@app.route('/zuser/<id>', methods=["GET", "PUT"])
def zuser(id=None):
    if request.method != 'GET':
        data = ujson.loads(request.data)

        if request.method == 'POST':
            existed = db.session.query(User).filter(
                User.username == data['username']).first()
            if existed is not None:
                raise w_exc.BadRequest(' existed username !')

            if 'username' not in data or 'password' not in data:
                raise w_exc.BadRequest(' username or password ?')
        else:
            if not id:
                raise w_exc.BadRequest('Update requie user id ')

            user_to_update = db.session.query(
                User).filter(User.id == id).first()

            if user_to_update is None:
                raise w_exc.BadRequest('invalid requie user id ')

            if user_to_update.username == data['username']:
                raise w_exc.BadRequest(' exist usernam !')

        values = {
            k: data[k] if k != 'password' else generate_password_hash(data[k])
            for k in data
        }
        user = User(**values)

        res = dict()
        if request.method == 'POST':
            res = insert_data(User, user)
            return jsonify(res), 200
        else:
            res = update_data(User, id, values)

        if hasattr(res, 'id'):
            return jsonify(res), 200
        else:
            # TODO: custom error msg
            w_exc.BadRequest(' cound not insert')

    res = get_data(User, id)
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4100)
