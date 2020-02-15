import pymysql
import datetime
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT


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


# 以下是调试用的
if __name__ == '__main__':
    query_all_activity_detail_by_eid("660001")
