import pymysql
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT
from util.util import is_str_empty


# 常量定义
ACTIVITY_ID_IDX = 0
ACTIVITY_TYPE_IDX = 1
ACTIVITY_SUBTYPE_IDX = 2
DATE_IDX = 4
MEAL_DELIVER_IDX = 9


def query_activity_list(from_date, to_date, group):
    """
    查询组信息列表

    若from_date 或 to_date不为空，则作为查询条件，其中包含from_date，不包含to_date

    :param from_date:
    :param to_date:
    :param group:
    :return:
    """

    # 组装sql
    sql = " select * from activity_info where `group` = %s "
    conditions = [group]

    if not is_str_empty(from_date):
        sql += " and date >= %s "
        conditions.append(from_date)
    if not is_str_empty(to_date):
        sql += " and date < %s "
        conditions.append(to_date)

    sql += " order by date, activityType, activitySubType asc"

    db = pymysql.connect(host=DB_HOST,
                         port=DB_PORT,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")
    try:
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            cursor.execute(sql, conditions)
            # 取第一条
            data = cursor.fetchall()
            return data
    finally:
        db.close()
