import pymysql
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT


# 查询用户
def create_activity_detail(eid):
    # db = pymysql.connect("rm-uf6zw3enwhk51ip15po.mysql.rds.aliyuncs.com", "lgtian_admin", "LGtian12&1",
    #                      "temperature_demo")

    db = pymysql.connect(host=DB_HOST,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "select activityDetailId, activityId,employeeId,quantity,createdBy,createdAt,updatedBy,updatedAt from activity_detail where employeeId = {0}".format(
                eid)
            cursor.execute(sql)
            # 取第一条
            data = cursor.fetchone()
            print(data)
            return data
    finally:
        db.close()


# 以下是调试用的
if __name__ == '__main__':
    create_activity_detail(660001)


