# from __future__ import (absolute_import, division,
#                         print_function, unicode_literals)
# from builtins import *

# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import flask_sqlalchemy as f_sa


# db = f_sa.SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     name = db.Column(db.String(64))

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class Customer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(140))
#     description = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     def __repr__(self):
#             return '<Cust {}>'.format(self.name)

# if __name__ == "__main__":
#     db.create_all()
