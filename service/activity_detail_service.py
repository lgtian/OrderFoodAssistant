import pymysql
import datetime
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT


# 插入活动明细
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

