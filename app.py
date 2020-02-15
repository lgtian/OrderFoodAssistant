from flask import Flask, request, render_template, redirect, url_for, Response
from service.user_service import query_user_pwd
from util.util import is_str_empty
from models import ActivityInfo, ActivityDetail, UserInfo
from exts import db
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT
from datetime import datetime
from datetime import timedelta
from constant import constants
import collections

app = Flask(__name__)
app.secret_key = '6789023yhfkjasd234'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ DB_USER+':'+DB_PWD+'@'+ DB_HOST + ':' + str(DB_PORT)+'/OrderFoodAssistant'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db.init_app(app)


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     return render_template('login.html')


# LOGIN BY COOKIE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        employee_id = request.cookies.get('EID')
        # 判断用户是否已登录
        if employee_id is not None:
            return redirect(url_for('home'))
        else:
            return render_template('login.html')

    # 登录操作
    employee_id = request.form['employeeId']
    pwd = request.form['pwd']

    if is_str_empty(employee_id) or is_str_empty(pwd):
        return render_template('login.html', message='incorrect employeeId')

    # 登录校验
    pwd_tuple = query_user_pwd(employee_id)
    if pwd_tuple is None:
        return render_template('login.html', message='incorrect employeeId')

    # 获取数据库密码
    db_password = pwd_tuple[0]
    # 密码判断
    if db_password != pwd:
        return render_template('login.html', message='incorrect password')

    # 登录成功
    response = Response(render_template('home.html', employeeId=employee_id))
    response.set_cookie('EID', employee_id, max_age=600)
    return response


@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('EID')
    return response


# 查询
@app.route('/orderList', methods=['POST', 'GET'])
def orderList():

    employee_id = request.cookies.get('EID')
    # 判断用户是否已登录
    if employee_id is None:
        return render_template('login.html')

    employee = UserInfo.query.filter(UserInfo.employeeId == employee_id).first()
    if employee is None:
        return render_template('login.html')

    #计算活动开始时间和结束时间
    now = datetime.now()
    start = now
    this_week_end = now.date() + timedelta(days=7 - now.weekday())
    this_week_friday = now.date() + timedelta(days=4 - now.weekday())
    this_week_friday_15 = datetime(this_week_friday.year, this_week_friday.month, this_week_friday.day, 15)

    isNextWeek = '0'
    if now.timestamp() > this_week_friday_15.timestamp():
        this_week_start = now.date() - timedelta(days=now.weekday())
        start = this_week_start + timedelta(days=7)
        this_week_end = this_week_end + timedelta(days=7)
        isNextWeek = '1'

    #查询活动列表
    activityInfos = ActivityInfo.query.filter(ActivityInfo.group == employee.group, ActivityInfo.expiredAt >= start, ActivityInfo.expiredAt < this_week_end).order_by(ActivityInfo.date).all()

    activityIds = []
    for activityInfo in activityInfos:
        activityIds.append(activityInfo.activityId)

    #查询活动详情列表
    activityDetails = ActivityDetail.query.filter(ActivityDetail.employeeId == employee.employeeId, ActivityDetail.activityId.in_(activityIds)).all()

    #组装返回报文
    orderdic = collections.OrderedDict()
    for activityInfo in activityInfos:
        orderKey = str(activityInfo.date) + activityInfo.activityType
        if orderKey in orderdic:
            row = orderdic[orderKey]
        else:
            row = {"activityType": constants.ACTIVITY_TYPE[activityInfo.activityType], "date": str(activityInfo.date) + "(" + constants.ISO_WEEK_DAY[activityInfo.date.isoweekday()] + ")", "ordered": "0"}
        for activityDetail in activityDetails:
            if activityInfo.activityId == activityDetail.activityId:
                row["activityId"] = activityInfo.activityId
                row["activitySubType"] = constants.ACTIVITY_SUB_TYPE[activityInfo.activitySubType]
                row["activityDetailId"] = activityDetail.activityDetailId
                row["total"] = activityDetail.quantity
                row["ordered"] = "1"
        orderdic[orderKey] = row

    orderList = []
    for v in orderdic.values():
        orderList.append(v)

    return {"list": orderList, "isNextWeek": isNextWeek}

if __name__ == '__main__':
    app.run(debug=True)
