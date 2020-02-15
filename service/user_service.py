import pymysql
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT


# 查询用户
def query_user_pwd(eid):
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
            sql = "select password from user_info where employeeId = {0}".format(eid)
            cursor.execute(sql)
            # 取第一条
            data = cursor.fetchone()
            return data
    finally:
        db.close()