#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import login_required, current_user
from flask import render_template, session, redirect, url_for, flash, abort, request, jsonify
from . import main
from .. import db
# from ..models import Equipment, FaultMsg, NewVal, FaultList
from ..models import Eqp
from ..util.db.mongo import Mongo_service

def code2state(state):
    if state == 1:
        return '预警状态'
    elif state == 2:
        return '设备故障'
    else:
        return '正常运行'


def codeToMes(code):
    if code == 1:
        return '信号丢失故障'
    elif code == 3:
        return '瞬时过流故障'
    elif code == 2:
        return '瞬时受力报警'
    elif code == 4:
        return '超出量程故障'
    elif code == 5:
        return '偏载报警'


def judgeFault(x):
    res = []
    x += 10000
    while x > 0:
        res.insert(0, x % 10)
        x = x // 10
    return res


@main.route('/', methods=['POST', 'GET'])
def index():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10]
    if current_user.is_authenticated:
        Eqp_new = Mongo_service(Eqp, current_user.factoryID.FID + 'eqp')
        if current_user.role_id.RID == 0:
            try:
                eqpList = Eqp_new.find_object()
            except Exception as e:
                flash(e)
                return render_template('500.html')
            # for eqp in eqpList:
                # FaultMsg.__table__.name = current_user.factoryID + eqp.id + 'faultmsg' + date
                # state = db.session.query(FaultMsg).order_by(FaultMsg.id.desc()).first()
                # setattr(eqp, 'state', code2state(state.eqpState))
            return render_template('main/MainPage.html', eqpList=eqpList)
        elif current_user.role_id.RID >= 1:
            eqpList = []
            eqpName = current_user.EqpID
            if eqpName:
                try:
                    for item in eqpName:
                        eqpList.append(Eqp_new.find_object(EID=item))
                except Exception as e:
                    flash(e)
                    return render_template('500.html')
                # for eqp in eqpList:
                #     FaultMsg.__table__.name = current_user.factoryID + eqp.id + 'faultmsg' + date
                #     state = db.session.query(FaultMsg).order_by(FaultMsg.id.desc()).first()
                #     setattr(eqp, 'state', code2state(state.eqpState))
            else:
                flash("请联系管理员为您添加设备！")
            return render_template('main/MainPage.html', eqpList=eqpList)
        else:
            pass
    return render_template('/main/MainPage.html')


@main.route('/Running/<string:EqpName>', methods=['POST', 'GET'])
@login_required
def Running(EqpName):
    return render_template('/main/RunningUI.html')

