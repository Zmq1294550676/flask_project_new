#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from app import creat_app, db
# from app.models import Role, User, Factory, Equipment, Supplier, countState, Thread, FaultList, Operation, NewVal, FaultMsg
from app.models import Role, User, Factory, Eqp, Supplier
from flask_script import Manager, Shell
from app.util.db.mongo import Mongo_service
from gevent import monkey
monkey.patch_all()

app = creat_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, Factory=Factory, Eqp=Eqp, Supplier=Supplier, Mongo_service=Mongo_service)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
