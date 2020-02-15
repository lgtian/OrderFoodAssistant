from flask import Flask, request, render_template, redirect, url_for, Response
from service.user_service import query_user_pwd
from service.activity_detail_service import create_activity_detail
from service.activity_detail_service import update_activity_detail
from service.activity_detail_service import query_activity_detail_by_eid_aid
from flask import jsonify
from util.util import is_str_empty

app = Flask(__name__)
app.secret_key = '6789023yhfkjasd234'


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

# 新增订餐明细接口
@app.route('/activity/detail/update', methods=['POST'])
def update_meal_order():
    eid = request.cookies.get('EID')

    if eid is None:
        employee_id = request.form.get('employeeId')
    else:
        employee_id = eid

    # 判断用户是否已登录
    if eid is None and employee_id is None:
        return render_template('login.html')

    # 获取订餐信息
    quantity = request.form.get('quantity')
    activity_id = request.form.get('activityId')

    # 活动信息校验
    if is_str_empty(activity_id):
        response = {"respCode": "9501", "respMsg": "incorrect activity_id"}
        return jsonify(response)

    # 订餐信息校验
    if quantity is None or int(quantity) <= 0:
        response = {"respCode": "9501", "respMsg": "incorrect quantity"}
        return jsonify(response)

    activity_detail = query_activity_detail_by_eid_aid(employee_id, activity_id)
    if activity_detail is None:
        response = {"respCode": "9501", "respMsg": "activity detail is not exist"}
        return jsonify(response)

    update_activity_detail(activity_id, employee_id, quantity)

    # 登录成功
    response = {"respCode": "1000", "respMsg": "success"}
    return response


if __name__ == '__main__':
    app.run(debug=True)