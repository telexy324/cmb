from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash

from . import main
from .forms import BindQueryForm, ChangeBindForm, AuthLogForm
from .. import db
import cx_Oracle
from ..models import Type9users1


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/bindquery', methods=['GET', 'POST'])
def bindQuery():
    form = BindQueryForm()

    if form.validate_on_submit():
        bqaccountid = form.faccountid.data
        sqlbq = 'select ac.account_id,ac.login_name,ac.isp_username,ac.isp_password,ac.isp_type from account_correspond ac where ac.isp_type=9 and ac.account_id='+bqaccountid
        bqurl = "bill/bill@beijing"
        bqconn = cx_Oracle.connect(bqurl)
        bqc = bqconn.cursor()
        bqresult = bqc.execute(sqlbq).fetchall()
        if len(bqresult) == 0:
            flash('未查询到匹配信息')
            return render_template('querybind.html', form=form)
        else:
            accountcorrespond = bqresult[0]
            return render_template('querybind.html', form=form, accountcorrespond=accountcorrespond)
    return render_template('querybind.html', form=form)


@main.route('/authlog', methods=['GET', 'POST'])
def authLog():
    form = AuthLogForm()

    if form.validate_on_submit():
        alaccountid = form.faccountid.data
        sqlal = 'select i.faccountid,i.fname,i.ispname,i.authtime,i.onlinetime from ispauthstarttbl i where i.faccountid=' + alaccountid
        alurl = "bill/bill@beijing"
        alconn = cx_Oracle.connect(alurl)
        alc = alconn.cursor()
        alresult = alc.execute(sqlal).fetchall()
        if len(alresult) == 0:
            flash('未查询到匹配信息')
            return render_template('authlog.html', form=form)
        else:
            ispauthstarttbl = alresult[0]
            return render_template('authlog.html', form=form, ispauthstarttbl=ispauthstarttbl)
    return render_template('authlog.html', form=form)


@main.route('/changebind', methods=['GET', 'POST'])
def changeBind():
    form = ChangeBindForm()

    if form.validate_on_submit():
        cbaccountid = form.faccountid.data
        sqlcb = 'select ac.account_id,ac.login_name,ac.isp_username,ac.isp_password,ac.isp_type from account_correspond ac where ac.account_id='+cbaccountid
        cburl = "bill/bill@beijing"
        cbconn = cx_Oracle.connect(cburl)
        cbc = cbconn.cursor()
        cbresult = cbc.execute(sqlcb).fetchall()
        if len(cbresult) == 0:
            sqlc = 'select u.account_id from user_info u where u.current_state=2 and u.community_id in \
                    (7491,5358,4199,5920,6171,6178,6363,6483,6206,7524,8024,8226,2817,2918,3717,3097,6112,6113,6111,6114,7398,2096,395,2577,2517) and u.account_id='+cbaccountid
            rec = cbc.execute(sqlc).fetchall()
            if len(rec) == 0:
                ispnameforupdate = Type9users1.query.order_by(Type9users1.id).filter_by(state=0).limit(1).all()
                Type9users1.query.filter_by(isp_username=ispnameforupdate[0].isp_username).update({'state': 1})
                sqlloginname = 'select login_name from user_info where account_id=' + cbaccountid
                cbloginname = cbc.execute(sqlloginname).fetchall()[0][0]
                sqlacmax = 'select max(id) from account_correspond where isp_type=9'
                cbnewid = cbc.execute(sqlacmax).fetchall()[0][0] + 1
                sqlintraw = 'insert into account_correspond values('
                sqlint = sqlintraw + str(cbnewid) + ',' + cbaccountid + ',\'' + cbloginname + '\',\'' + ispnameforupdate[0].isp_username + '\',\''+ispnameforupdate[0].isp_password+'\',9)'
                cbc.execute(sqlint)
                cbconn.commit()
                flash('绑定成功! 方宽ID号:' + str(cbaccountid) + ' 此用户不在目标小区或未开通! 现联通用户名:' + ispnameforupdate[0].isp_username)
            else:
                ispnameforupdate = Type9users1.query.order_by(Type9users1.id).filter_by(state=0).limit(1).all()
                Type9users1.query.filter_by(isp_username=ispnameforupdate[0].isp_username).update({'state': 1})
                sqlloginname = 'select login_name from user_info where account_id=' + cbaccountid
                cbloginname = cbc.execute(sqlloginname).fetchall()[0][0]
                sqlacmax = 'select max(id) from account_correspond where isp_type=9'
                cbnewid = cbc.execute(sqlacmax).fetchall()[0][0] + 1
                sqlintraw = 'insert into account_correspond values('
                sqlint = sqlintraw + str(
                    cbnewid) + ',' + cbaccountid + ',\'' + cbloginname + '\',\'' + ispnameforupdate[0].isp_username + '\',\''+ispnameforupdate[0].isp_password+'\',9)'
                cbc.execute(sqlint)
                cbconn.commit()
                flash('绑定成功! 方宽ID号:' + str(cbaccountid) + ' 现联通用户名:' + ispnameforupdate[0].isp_username)

        else:
            if cbresult[0][4] == 9:
                ispnameforupdate = Type9users1.query.order_by(Type9users1.id).filter_by(state=0).limit(1).all()
                Type9users1.query.filter_by(isp_username=ispnameforupdate[0].isp_username).update({'state':1})
                isporiginname = cbresult[0][2]
                Type9users1.query.filter_by(isp_username=isporiginname).update({'state': 2})
                db.session.commit()
                sqlupdatealready = 'update account_correspond set isp_username=\'' + ispnameforupdate[0].isp_username + '\',isp_password=\''+ispnameforupdate[0].isp_password+'\' where account_id=' + str(cbresult[0][0])
                cbc.execute(sqlupdatealready)
                cbconn.commit()
                flash('换绑成功! 方宽ID号:'+str(cbaccountid)+' 原联通用户名:'+isporiginname+' 现联通用户名:'+ispnameforupdate[0].isp_username)
                return render_template('changebind.html', form=form)
            else:
                ispnameforupdate = Type9users1.query.order_by(Type9users1.id).filter_by(state=0).limit(1).all()
                Type9users1.query.filter_by(isp_username=ispnameforupdate[0].isp_username).update({'state': 1})
                db.session.commit()
                sqlupdatealready = 'update account_correspond set isp_username=\'' + ispnameforupdate[0].isp_username + '\',isp_password=\''+ispnameforupdate[0].isp_password+'\',isp_type=9 where account_id=' + str(cbresult[0][0])
                cbc.execute(sqlupdatealready)
                cbconn.commit()
                flash('换绑成功! 方宽ID号:' + str(cbaccountid) + ' 此用户为原有合作帐号, 现联通用户名:' + ispnameforupdate[0].isp_username)
                return render_template('changebind.html', form=form)

        return render_template('changebind.html', form=form)
    return render_template('changebind.html', form=form)
