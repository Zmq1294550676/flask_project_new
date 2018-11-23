#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from flask import current_app


# 记载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class Permission:
    Operator = 2
    Engineer = 1
    ADMINSTER = 0

class Role(db.Document):
    RID = db.IntField()
    name = db.StringField(max_length=64, unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class Factory(db.Document):
    FID = db.StringField(max_length=20, unique=True)
    address = db.StringField(max_length=40)
    responsor = db.StringField(max_length=20)
    meta = {'indexes': ['FID']}


# 每个工厂一张，命名：FacID + Sup
class Supplier(db.Document):
    contact = db.StringField(max_length=20)
    SID = db.StringField(max_length=20, unique_with="contact")
    info = db.StringField(max_length=100)
    meta = {'indexes': [('SID', 'contact')]}


# 每个工厂一张，命名：FacID + EQP
class Eqp(db.Document):
    EID = db.StringField(max_length=20, unique=True)
    place = db.StringField(max_length=20)
    supplier = db.DictField()
    meta = {'indexes': ['EID']}


class User(UserMixin, db.Document):
    UID = db.StringField(max_length=64, unique=True)
    role_id = db.ReferenceField(Role)
    password_hash = db.StringField(max_length=128)
    factoryID = db.ReferenceField(Factory, reverse_delete_rule=db.CASCADE)
    Eqp = db.ListField(db.StringField(max_length=20))
    meta = {'indexes': ['UID']}

    # 新增密码散列化
    @property
    def password(self):
        raise AttributeError('password is not a readable attr')

    def set_pass(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
