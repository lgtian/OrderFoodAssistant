from flask import Flask, request, render_template, redirect, url_for
from service.activity_detail_service import create_activity_detail
from service.activity_detail_service import query_activity_detail_by_eid_aid
from service.activity_detail_service import query_all_activity_detail_by_eid
from service.activity_detail_service import update_activity_detail
from service.activity_detail_service import query_activity_detail_by_aid
from service.activity_detail_service import delete_activity_detail
from flask import jsonify
from models import ActivityInfo, ActivityDetail, UserInfo
from exts import db
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT
from datetime import datetime
from datetime import timedelta
from constant import constants
from service.user_service import query_user, USER_GROUP_IDX, USER_PWD_IDX, USER_NAME_IDX
from util.util import is_str_empty, join_dict_elems, get_week_day
import service.activity_service
from service.activity_detail_service import query_activity_detail_list, QUANTITY_IDX

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + DB_USER + ':' + DB_PWD + '@' + DB_HOST + ':' + str(
    DB_PORT) + '/OrderFoodAssistant'
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SECRET_KEY'] = "this is a secret_key"
db.init_app(app)


@app.route('/menu')
def menu():
    imgUrl = 'https://res.cc.cmbimg.com/fsp/File/G20200214G1338672663G32312D32372D5C385C375C.DAT';
    return render_template('menu.html', imgUrl=imgUrl)


@app.route('/order_detail', methods=['GET', 'POST'])
def order_detail():
    """
    获取订单详情

    返回样例：
    activity = {
        "activityType": "午餐",
        "date": "2020-02-18 (周二)",
        "deliveryman": '232422',
        "totalPrice": '40',
        "summaryList": [
            {
                "totalPrice": '20',
                "desc": '11元套餐 x2'
            },
            {
                "totalPrice": '20',
                "desc": '16元套餐 x2'
            }
        ],
        "memberList": [{
                "employeeId": "888888",
                "summary": "11元套餐 x2"
            },
            {
                "employeeId": "888888",
                "summary": "11元套餐 x2"
            },
            {
                "employeeId": "888888",
                "summary": "16元套餐 x2"
            },
            {
                "employeeId": "888888",
                "summary": "11元套餐 x2"
            }
        ]
    }
    """
    employee_id = request.cookies.get('EID')
    group_user = request.cookies.get('UGP')

    # 登录校验
    if is_str_empty(employee_id):
        return redirect(url_for('login'))

    # 查询组信息
    employee = UserInfo.query.filter(UserInfo.employeeId == employee_id).first()
    if employee is None:
        return redirect(url_for('login'))

    activity_type = request.values.get('activityType')
    date = request.values.get('date')

    # 查询活动信息
    activity_infos = ActivityInfo.query.filter(ActivityInfo.group == employee.group,
                                               ActivityInfo.date == date,
                                               ActivityInfo.activityType == activity_type). \
        order_by(ActivityInfo.activityId).all()

    activity_id_info_dict = {}
    # 每种子活动的数量
    activity_id_total_cnt_dict = {}
    # activity_id_product_dict = {}
    deliver_man = ''
    for activity_info in activity_infos:
        activity_id_info_dict[activity_info.activityId] = activity_info
        activity_id_total_cnt_dict[activity_info.activityId] = 0
        # product_info = ProduceInfo.query.filter(ProduceInfo.productType == activity_info.activityType,
        #                                         ProduceInfo.productSubType == activity_info.activitySubType).first()
        # activity_id_product_dict[activity_info.activityId] = product_info
        if is_str_empty(deliver_man) and not is_str_empty(activity_info.mealDeliver):
            deliver_man = activity_info.mealDeliver

    # 查询活动详情列表
    activity_details = ActivityDetail.query.filter(ActivityDetail.activityId.in_(activity_id_info_dict.keys())) \
        .order_by(ActivityDetail.activityId).all()

    member_dict = {}
    for detail in activity_details:
        # 对应活动
        activity_info = activity_id_info_dict[int(detail.activityId)]

        # 对同一用户的多种活动进行组合
        member_elem = member_dict.get(detail.employeeId)
        if member_elem is None:
            activity_user_tuple = query_user(detail.employeeId)
            member_elem = {
                "employeeId": detail.employeeId,
                "employeeName": activity_user_tuple[USER_NAME_IDX],
                "summary": [gen_summary_elem(constants.ACTIVITY_SUB_TYPE[activity_info.activitySubType],
                                             detail.quantity)]
            }
        else:
            summary = member_elem.get("summary")
            summary.append(gen_summary_elem(constants.ACTIVITY_SUB_TYPE[activity_info.activitySubType],
                                            detail.quantity))

        member_dict[detail.employeeId] = member_elem
        activity_id_total_cnt_dict[activity_info.activityId] += detail.quantity

    summary_list = []
    total_price = 0
    for activity_id, total_cnt in activity_id_total_cnt_dict.items():
        # product_info = activity_id_product_dict[activity_id]
        activity_info = activity_id_info_dict[activity_id]
        activity_total_price = total_cnt * int(activity_info.activitySubType)
        summary_list.append({
            "totalPrice": str(activity_total_price),
            "desc": constants.ACTIVITY_SUB_TYPE[activity_info.activitySubType] + " x" + str(total_cnt)
        })
        total_price += activity_total_price

    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    # 组装返回
    activity = {
        "activityType": activity_type,
        "date": date + "（" + get_week_day(date_obj) + "）",
        "deliveryman": deliver_man,
        "totalPrice": str(total_price),
        "summaryList": summary_list,
        "memberList": member_dict.values()
    }

    return render_template('order-detail.html', activity=activity, group_user=group_user)


# LOGIN BY COOKIE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        employee_id = request.cookies.get('EID')
        # 判断用户是否已登录
        if employee_id is not None:
            return redirect(url_for('order'))
        else:
            return render_template('login.html')

    # 登录操作
    employee_id = request.form['employeeId']
    pwd = request.form['pwd']

    if is_str_empty(employee_id) or is_str_empty(pwd):
        return render_template('login.html', message='员编错误或未注册')

    # 登录校验
    user_tuple = query_user(employee_id)
    if user_tuple is None:
        return render_template('login.html', message='员编错误或未注册')

    # 获取数据库密码
    db_password = user_tuple[USER_PWD_IDX]
    # 密码判断
    if db_password != pwd:
        return render_template('login.html', message='密码错误')

    # 登录成功
    response = redirect(url_for('login'))
    response.set_cookie('EID', employee_id, max_age=2 * 24 * 3600)
    response.set_cookie('UGP', user_tuple[USER_GROUP_IDX], max_age=2 * 24 * 3600)
    return response


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('EID')
    return response


# 新增订餐明细接口
@app.route('/activity/detail/add', methods=['POST'])
def create_meal_order():
    """
    接口入参
    employeeId  |string|O|员工编号
    quantity    |int   |M|订餐数量
    activityId  |int   |M|活动id

    接口出参
    respCode             |string|M|返回码
    respMsg              |string|M|返回话术

    返回报文样例
    {
        "respCode": "1000",
        "respMsg": "success"
    }
    """
    eid = request.cookies.get('EID')

    if eid is None:
        employee_id = request.form.get('employeeId')
    else:
        employee_id = eid

    # 判断用户是否已登录
    if eid is None and employee_id is None:
        return redirect(url_for('login'))

    created_by = employee_id
    # 获取订餐信息
    quantity = request.form.get('quantity')
    activity_id = request.form.get('activityId')

    # 活动信息校验
    if is_str_empty(activity_id):
        response = {"respCode": "9501", "respMsg": "incorrect activity_id"}
        return jsonify(response)
    activity_id = int(activity_id)

    quantity = int(quantity)
    # 订餐信息校验
    if quantity is None or quantity <= 0:
        response = {"respCode": "9501", "respMsg": "incorrect quantity"}
        return jsonify(response)

    create_activity_detail(activity_id, employee_id, quantity, created_by)

    # 登录成功
    return redirect(url_for('order'))


# 查询订餐明细接口
@app.route('/activity/detail/query', methods=['POST'])
def query_meal_order():
    """
    接口入参
    employeeId  |string|O|员工编号
    activityId  |int   |O|活动id

    接口出参
    respCode             |string|M|返回码
    respMsg              |string|M|返回话术
    activityDetail       |string|O|某个订餐明细，入参传activityId，则出现该字段
    activityDetailList   |string|O|若干个订餐明细的集合，入参不传activityId，则出现该字段
        activityDetailId        |int   |O|活动详情id
        activityId              |int   |O|活动id
        employeeId              |string|O|员工编号
        quantity                |int   |O|订餐数量
        createdBy               |string|O|创建者员工编号
        createdAt               |string|O|创建时间
        updatedBy               |string|O|更新者员工编号
        updatedAt               |string|O|更新时间


    返回报文样例
    {
    "activityDetailList": [
        [
            1,
            1,
            "660001",
            1,
            "660001",
            "Sat, 15 Feb 2020 21:22:11 GMT",
            "660001",
            "Sat, 15 Feb 2020 21:22:11 GMT"
        ],
        [
            2,
            1,
            "660001",
            1,
            "660001",
            "Sat, 15 Feb 2020 21:30:41 GMT",
            "660001",
            "Sat, 15 Feb 2020 21:30:41 GMT"
        ]
    ],
    "respCode": "1000",
    "respMsg": "success"
    }
    """
    eid = request.cookies.get('EID')

    if eid is None:
        employee_id = request.form.get('employeeId')
    else:
        employee_id = eid

    # 判断用户是否已登录
    if eid is None and employee_id is None:
        return redirect(url_for('login'))

    # 获取订餐活动的id信息
    activity_id = request.form.get('activityId')

    # 活动信息校验
    if is_str_empty(activity_id):
        activity_detail_list = query_all_activity_detail_by_eid(employee_id)
        response = {"respCode": "1000", "respMsg": "success", "activityDetailList": activity_detail_list}
        return jsonify(response)

    activity_id = int(activity_id)
    activity_detail = query_activity_detail_by_eid_aid(employee_id, activity_id)
    response = {"respCode": "1000", "respMsg": "success", "activityDetail": activity_detail}
    return jsonify(response)


# 修改订餐明细接口
@app.route('/activity/detail/update', methods=['POST'])
def update_meal_order():
    """
       接口入参：
       employeeId|String|M|员工编号 --注意该值从cookie中去
       quantity|String|M|数量
       activity_detail_id|String|M|活动详情id

       接口出参：
       respCode|String|M|响应码
       respMsg|String|M|响应话术

       返回报文样例：
       {"respCode":"1000","respMsg":"success"}
       {"respCode":"9501","respMsg":"activity_detail_id is null"}
    """
    eid = request.cookies.get('EID')

    if eid is None:
        employee_id = request.form.get('employeeId')
    else:
        employee_id = eid

    # 判断用户是否已登录
    if eid is None and employee_id is None:
        return redirect(url_for('login'))

    # 获取订餐信息
    quantity = request.form.get('quantity')
    activity_detail_id = request.form.get('activityDetailId')

    # 活动信息校验
    if is_str_empty(activity_detail_id):
        response = {"respCode": "9501", "respMsg": "activity_detail_id is null"}
        return jsonify(response)

    # 订餐信息校验
    if quantity is None or int(quantity) <= 0:
        response = {"respCode": "9501", "respMsg": "incorrect quantity"}
        return jsonify(response)

    activity_detail = query_activity_detail_by_aid(activity_detail_id)
    if activity_detail is None:
        response = {"respCode": "9501", "respMsg": "activity detail is not exist"}
        return jsonify(response)

    update_activity_detail(activity_detail_id, employee_id, quantity)

    # 更新成功
    return redirect(url_for('order'))


# 删除订餐明细接口
@app.route('/activity/detail/delete', methods=['POST'])
def delete_meal_order():
    """
       接口入参：
       employeeId|String|M|员工编号 -- --注意该值从cookie中去
       activity_detail_id|String|M|活动详情id

       接口出参：
       respCode|String|M|响应码
       respMsg|String|M|响应话术

       返回报文样例：
       {"respCode":"1000","respMsg":"success"}
       {"respCode":"9501","respMsg":"activity_detail_id is null"}
    """
    eid = request.cookies.get('EID')

    if eid is None:
        employee_id = request.form.get('employeeId')
    else:
        employee_id = eid

    # 判断用户是否已登录
    if eid is None and employee_id is None:
        return redirect(url_for('login'))

    # 获取订餐信息
    activity_detail_id = request.form.get('activityDetailId')

    # 活动信息校验
    if is_str_empty(activity_detail_id):
        response = {"respCode": "9501", "respMsg": "activity_detail_id is null"}
        return jsonify(response)

    activity_detail = query_activity_detail_by_aid(activity_detail_id)
    if activity_detail is None:
        response = {"respCode": "9501", "respMsg": "activity detail is not exist"}
        return jsonify(response)

    delete_activity_detail(activity_detail_id)

    # 登录成功
    return redirect(url_for('order'))


# 订餐
@app.route('/order', methods=['POST', 'GET'])
def order():
    """
     订餐接口

    入参：
        EID      当前登录人id，从cookie中取

    出参：
        isNextWeek 是否展示下周 1-是  0-否
        activity_list 链表，包含以下元素
            activityType 活动类型 如 午餐
            date 活动日期 如 2020-02-18(周二)
            ordered 是否已预订 1-已预订 0-未预订
            activityId 活动id
            activitySubType 活动子类型 如：11元套餐
            activityDetailId 活动详情id
            total 总数

        实例报文：
            {
             'activity_list': [{
             'activityType': '午餐',
             'date': '2020-02-17(周一)',
             'ordered': '1',
             'activityId': 2,
             'activitySubType': '16元套餐',
             'activityDetailId': 1,
             'total': 1
             },
             {
             'activityType': '晚餐',
             'date': '2020-02-21(周五)',
             'ordered': '0'
             }],
             'isNextWeek': '1'
             }
    """
    employee_id = request.cookies.get('EID')
    # 判断用户是否已登录
    if employee_id is None:
        return redirect(url_for('login'))

    employee = UserInfo.query.filter(UserInfo.employeeId == employee_id).first()
    if employee is None:
        return redirect(url_for('login'))

    # 计算活动开始时间和结束时间
    now = datetime.now()
    start = now
    end = now + timedelta(days=7)
    # 查询7天活动列表
    activityInfos = ActivityInfo.query.filter(ActivityInfo.group == employee.group, ActivityInfo.expiredAt >= start,
                                              ActivityInfo.expiredAt < end).order_by(ActivityInfo.date,
                                                                                     ActivityInfo.activityType,
                                                                                     ActivityInfo.activitySubType).all()

    activityIds = []
    for activityInfo in activityInfos:
        activityIds.append(activityInfo.activityId)

    # 查询活动详情列表
    activityDetails = ActivityDetail.query.filter(ActivityDetail.employeeId == employee.employeeId,
                                                  ActivityDetail.activityId.in_(activityIds)).all()

    # 组装返回报文
    orderList = []
    for activityInfo in activityInfos:
        row = {"activityType": activityInfo.activityType,
               "date": str(activityInfo.date) + "（" + constants.ISO_WEEK_DAY[activityInfo.date.isoweekday()] + "）",
               "ordered": "0", "activitySubType": constants.ACTIVITY_SUB_TYPE[activityInfo.activitySubType],
               "activityId": activityInfo.activityId}
        for activityDetail in activityDetails:
            if activityInfo.activityId == activityDetail.activityId:
                # row["activityId"] = activityInfo.activityId
                # row["activitySubType"] = constants.ACTIVITY_SUB_TYPE[activityInfo.activitySubType]
                row["activityDetailId"] = activityDetail.activityDetailId
                row["total"] = activityDetail.quantity
                row["ordered"] = "1"
        orderList.append(row)

    return render_template('order.html', activity_list=orderList)


@app.route('/gather_activities', methods=['GET', 'POST'])
def gather_activities():
    """
    订单汇总接口

    入参：
        EID      当前登录人id，从cookie中取

    出参：
        todayList 链表，包含以下元素
            title 如 午餐-2020-02-15
            summary 如 11元套餐 X11, 16元套餐 X10
            mealDeliver 送餐人id
            date
            activityType

        weekList 链表，包含以下元素
            title 如 午餐-2020-02-15
            summary 如 11元套餐 X11, 16元套餐 X10
            mealDeliver 送餐人id
            date
            activityType
    """

    employee_id = request.cookies.get('EID')
    group_user = request.cookies.get('UGP')

    # 登录校验
    if employee_id is None or is_str_empty(employee_id):
        return redirect(url_for('login'))

    # 查询组信息
    user_tuple = query_user(employee_id)
    if user_tuple is None:
        return redirect(url_for('login'))

    group = user_tuple[USER_GROUP_IDX]

    today_begin = datetime.now().date()
    today_end = today_begin + timedelta(days=1)
    today_list = do_gather_activity(today_begin, today_end, group)

    future_begin = today_end
    future_end = today_begin + timedelta(days=7)
    future_list = do_gather_activity(future_begin, future_end, group)

    return render_template('statistics.html', today_list=today_list, week_list=future_list, group_user=group_user)


def do_gather_activity(from_date, end_date, group):
    # 查询活动信息
    activity_tuple_list = service.activity_service.query_activity_list(from_date, end_date, group)
    if activity_tuple_list is None or len(activity_tuple_list) == 0:
        activity_tuple_list = []

    # 汇总每天的信息
    res_dict = {}
    for activity_tuple in activity_tuple_list:
        activity_id = activity_tuple[service.activity_service.ACTIVITY_ID_IDX]

        # 拼接title，如午餐 * 2020-02-15
        title = gen_summary_title(activity_tuple[service.activity_service.ACTIVITY_TYPE_IDX]
                                  , activity_tuple[service.activity_service.DATE_IDX])

        # 查询详情信息
        activity_detail_tuple_list = query_activity_detail_list(activity_id)

        # 汇总当前订餐总数
        activity_subtype_cnt = 0
        if activity_detail_tuple_list is not None and len(activity_detail_tuple_list) > 0:
            for activity_detail_tuple in activity_detail_tuple_list:
                activity_subtype_cnt += int(activity_detail_tuple[QUANTITY_IDX])

        # 判断记录是否已有
        one_day_summary_dict = res_dict.get(title)
        if one_day_summary_dict is None:
            one_day_summary_dict = {'title': title}

        # 记录subType及数量
        subtype_desc = constants.ACTIVITY_SUB_TYPE[activity_tuple[service.activity_service.ACTIVITY_SUBTYPE_IDX]]
        one_day_summary_dict[subtype_desc] = activity_subtype_cnt

        # 记录领餐人，没有才更新
        meal_deliver = one_day_summary_dict.get('mealDeliver')
        if meal_deliver is None or is_str_empty(meal_deliver):
            one_day_summary_dict['mealDeliver'] = activity_tuple[service.activity_service.MEAL_DELIVER_IDX]

        # 设置日期
        one_day_summary_dict['date'] = activity_tuple[service.activity_service.DATE_IDX]
        # 设置类型
        one_day_summary_dict['activityType'] = activity_tuple[service.activity_service.ACTIVITY_TYPE_IDX]

        res_dict[title] = one_day_summary_dict

    # 汇总信息排序
    res_list = []
    for activity_tuple in activity_tuple_list:
        title = gen_summary_title(activity_tuple[service.activity_service.ACTIVITY_TYPE_IDX]
                                  , activity_tuple[service.activity_service.DATE_IDX])
        tmp_dict = res_dict.get(title)
        # 格式化信息，防止重复数据
        if tmp_dict is not None and tmp_dict.get('title') is not None:
            format_dict = {
                'title': tmp_dict.pop('title'),
                'mealDeliver': tmp_dict.pop('mealDeliver'),
                'date': datetime.strftime(tmp_dict.pop('date'), "%Y-%m-%d"),
                'activityType': tmp_dict.pop('activityType'),
                'summary': join_dict_elems(tmp_dict, ' x', ', ')
            }
            res_list.append(format_dict)
    return res_list


@app.route('/allActivities', methods=['GET', 'POST'])
def all_activities():
    """
    全部订单接口

    入参：
        fromDate String|O| 开始查询时间
        endDate  String|O| 结束查询时间
        EID      当前登录人id，从cookie中取

    出参：
        summaryList 链表，包含以下元素
            title 如 午餐-2020-02-15
            summary 如 11元套餐 X11, 16元套餐 X10
            mealDeliver 送餐人id
            date
            activityType

    入参样例：
        EID:1
        //fromDate:2020-02-15
        endDate:2020-02-20

    返回样例：
        activity_summary_list:[{'title': '午餐 * 2020-02-15(星期六)', 'mealDeliver': '111', 'summary': ', 11元套餐 x4, 16元套餐 x1'}, {'title': '晚餐 * 2020-02-15(星期六)', 'mealDeliver': None, 'summary': ', 11元套餐 x0, 16元套餐 x0'}]
    """

    employee_id = request.cookies.get('EID')
    # employee_id = request.values.get('EID')
    from_date = request.values.get('fromDate')
    end_date = request.values.get('endDate')

    # 登录校验
    if employee_id is None or is_str_empty(employee_id):
        return redirect(url_for('login'))

    # 查询组信息
    user_tuple = query_user(employee_id)
    if user_tuple is None:
        return redirect(url_for('login'))

    group = user_tuple[USER_GROUP_IDX]

    # 查询活动信息
    activity_tuple_list = service.activity_service.query_activity_list(from_date, end_date, group)
    if activity_tuple_list is None or len(activity_tuple_list) == 0:
        return render_template('statistics-all.html', message='no info')

    # 汇总每天的信息
    res_dict = {}
    for activity_tuple in activity_tuple_list:
        activity_id = activity_tuple[service.activity_service.ACTIVITY_ID_IDX]

        # 拼接title，如午餐 * 2020-02-15
        title = gen_summary_title(activity_tuple[service.activity_service.ACTIVITY_TYPE_IDX]
                                  , activity_tuple[service.activity_service.DATE_IDX])

        # 查询详情信息
        activity_detail_tuple_list = query_activity_detail_list(activity_id)

        # 汇总当前订餐总数
        activity_subtype_cnt = 0
        if activity_detail_tuple_list is not None and len(activity_detail_tuple_list) > 0:
            for activity_detail_tuple in activity_detail_tuple_list:
                activity_subtype_cnt += int(activity_detail_tuple[QUANTITY_IDX])

        # 判断记录是否已有
        one_day_summary_dict = res_dict.get(title)
        if one_day_summary_dict is None:
            one_day_summary_dict = {'title': title}

        # 记录subType及数量
        subtype_desc = constants.ACTIVITY_SUB_TYPE[activity_tuple[service.activity_service.ACTIVITY_SUBTYPE_IDX]]
        one_day_summary_dict[subtype_desc] = activity_subtype_cnt

        # 记录日期
        one_day_summary_dict['date'] = activity_tuple[service.activity_service.DATE_IDX]

        # 记录领餐人，没有才更新
        meal_deliver = one_day_summary_dict.get('mealDeliver')
        if meal_deliver is None or is_str_empty(meal_deliver):
            one_day_summary_dict['mealDeliver'] = activity_tuple[service.activity_service.MEAL_DELIVER_IDX]

        # 设置类型
        one_day_summary_dict['activityType'] = activity_tuple[service.activity_service.ACTIVITY_TYPE_IDX]

        res_dict[title] = one_day_summary_dict

    # 汇总信息排序
    res_list = []
    for activity_tuple in activity_tuple_list:
        title = gen_summary_title(activity_tuple[service.activity_service.ACTIVITY_TYPE_IDX]
                                  , activity_tuple[service.activity_service.DATE_IDX])
        tmp_dict = res_dict.get(title)
        # 格式化信息，防止重复数据
        if tmp_dict is not None and tmp_dict.get('title') is not None:
            format_dict = {
                'title': tmp_dict.pop('title'),
                'mealDeliver': tmp_dict.pop('mealDeliver'),
                'date': datetime.strftime(tmp_dict.pop('date'), "%Y-%m-%d"),
                'activityType': tmp_dict.pop('activityType'),
                'summary': join_dict_elems(tmp_dict, ' x', ', ')
            }
            res_list.append(format_dict)

    return render_template('statistics-all.html', activity_list=res_list)


def gen_summary_title(prefix, date):
    return str(prefix) + " · " + str(date) + ' （' + get_week_day(date) + '） '


def gen_summary_elem(prefix, quantity):
    if quantity >= 0:
        return prefix + " x" + str(quantity)
    else:
        return ''


# 批量添加活动接口，暂时不开放
# @app.route('/addActivity', methods=['POST', 'GET'])
# def addActivity():
#     startDate = request.args.get("startDate")
#     endDate = request.args.get("endDate")
#     groupName = request.args.get("groupName")
#
#     if startDate is None or endDate is None or groupName is None:
#         return "param error"
#     connection = db.engine.raw_connection()
#     cursor = connection.cursor()
#     cursor.callproc('sp_batch_create_actiity', [startDate, endDate, groupName])
#     return "success"

if __name__ == '__main__':
    app.run(debug=True)
