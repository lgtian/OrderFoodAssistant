import pymysql
import datetime
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT


# 常量定义
QUANTITY_IDX = 3


# 新建活动明细
def create_activity_detail(activity_id, employee_id, quantity, created_by):

    db = pymysql.connect(host=DB_HOST,
                         port=DB_PORT,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        updated_by = created_by
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_at = dt
        updated_at = dt

        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "INSERT INTO activity_detail(activityId,employeeId,quantity," \
                  "createdBy,createdAt,updatedBy,updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            values = (activity_id, employee_id, quantity, created_by, created_at, updated_by, updated_at)
            cursor.execute(sql, values)
            db.commit()
            cursor.close()

    finally:
        db.close()


# 查询用户所有的订餐明细
def query_all_activity_detail_by_eid(employee_id):

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
            sql = "SELECT * FROM activity_detail WHERE employeeId = %s"
            values = (employee_id)
            cursor.execute(sql, values)
            # 取第一条
            data = cursor.fetchall()
            print(data)
            cursor.close()
            return data
    finally:
        db.close()

#
def query_activity_detail_by_aid(activity_detail_id):

    db = pymysql.connect(host=DB_HOST,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "SELECT * FROM activity_detail WHERE activityDetailId = %s"
            values = (activity_detail_id)
            cursor.execute(sql, values)
            # 取第一条
            data = cursor.fetchone()
            return data
    finally:
        db.close()

# 更新活动明细
def update_activity_detail(activity_detail_id, employee_id, quantity):

    db = pymysql.connect(host=DB_HOST,
                         port=DB_PORT,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "UPDATE activity_detail SET quantity = %s, updatedBy = %s, updatedAt = %s WHERE activityDetailId = %s"
            values = (quantity, employee_id, dt, activity_detail_id)
            cursor.execute(sql, values)
            db.commit()
            cursor.close()

    finally:
        db.close()

# 删除活动明细
def delete_activity_detail(activity_detail_id):

    db = pymysql.connect(host=DB_HOST,
                         port=DB_PORT,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "DELETE FROM activity_detail WHERE activityDetailId = %s"
            values = (activity_detail_id)
            cursor.execute(sql, values)
            db.commit()
            cursor.close()

    finally:
        db.close()

# 以下是调试用的
if __name__ == '__main__':
    query_all_activity_detail_by_eid("660001")

def query_activity_detail_list(activity_id):
    """
    根据id查询活动详情

    :param activity_id:
    :return:
    """

    # 组装sql
    sql = " select * from activity_detail where activityId = {0} ".format(activity_id)

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
            cursor.execute(sql)
            # 取第一条
            data = cursor.fetchall()
            return data
    finally:
        db.close()
