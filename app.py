from flask import Flask, request, render_template, redirect, url_for, Response
from service.user_service import query_user_pwd
from service.activity_detail_service import create_activity_detail
from flask import jsonify
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


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template('statistics.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    activity_list = [{
         "activityId": 11,
         "activityType": "午餐",
         "activitySubType": "11元套餐",
         "date": "2020-02-18 (周二)",
         "activityDetailId": 111,
         "total":"10",
         "ordered": "1"
        },
        {
         "activityType": "晚餐",
         "date": "2020-02-19 (周三)",
         "ordered": "0"
        },
        {
            "activityId": 11,
            "activityType": "午餐",
            "activitySubType": "11元套餐",
            "date": "2020-02-18 (周二)",
            "activityDetailId": 111,
            "total": "10",
            "ordered": "1"
        },
        {
            "activityType": "晚餐",
            "date": "2020-02-19 (周三)",
            "ordered": "0"
        },
        {
            "activityId": 11,
            "activityType": "午餐",
            "activitySubType": "11元套餐",
            "date": "2020-02-18 (周二)",
            "activityDetailId": 111,
            "total": "10",
            "ordered": "1"
        },
        {
            "activityType": "晚餐",
            "date": "2020-02-19 (周三)",
            "ordered": "0"
        },
        {
            "activityId": 11,
            "activityType": "午餐",
            "activitySubType": "11元套餐",
            "date": "2020-02-18 (周二)",
            "activityDetailId": 111,
            "total": "10",
            "ordered": "1"
        },
        {
            "activityType": "晚餐",
            "date": "2020-02-19 (周三)",
            "ordered": "0"
        },
        {
            "activityId": 11,
            "activityType": "午餐",
            "activitySubType": "11元套餐",
            "date": "2020-02-18 (周二)",
            "activityDetailId": 111,
            "total": "10",
            "ordered": "1"
        }
    ]
    return render_template('order.html', activity_list=activity_list, order_this_week=True)


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


# 新增订餐明细接口
@app.route('/activity/detail/add', methods=['POST'])
def create_meal_order():
    eid = request.cookies.get('EID')

    if eid is None:
        employee_id = request.form['employeeId']
    else:
        employee_id = eid

    # 判断用户是否已登录
    if eid is None and employee_id is None:
        return render_template('login.html')

    created_by = employee_id
    # 获取订餐信息
    quantity = request.form['quantity']
    activity_id = request.form['activityId']

    # 活动信息校验
    if is_str_empty(activity_id):
        response = {"respCode": "9501", "respMsg": "incorrect activity_id"}
        return jsonify(response)

    quantity = int(quantity)
    # 订餐信息校验
    if quantity is None or quantity <= 0:
        response = {"respCode": "9501", "respMsg": "incorrect quantity"}
        return jsonify(response)

    create_activity_detail(activity_id, employee_id, quantity, created_by)

    # 登录成功
    response = {"respCode": "1000", "respMsg": "success"}
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