import pymysql
from config.config import DB_HOST, DB_USER, DB_PWD, DB_PORT

# 常量
USER_NAME_IDX = 1
USER_PWD_IDX = 2
USER_GROUP_IDX = 3


# 查询用户
def query_user_pwd(eid):
    db = pymysql.connect(host=DB_HOST,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "select password from user_info where employeeId = '{0}'".format(eid)
            cursor.execute(sql)
            # 取第一条
            data = cursor.fetchone()
            return data
    finally:
        db.close()


# 查询用户组信息
def query_user(eid):
    db = pymysql.connect(host=DB_HOST,
                         user=DB_USER,
                         password=DB_PWD,
                         database="OrderFoodAssistant",
                         charset="utf8")

    try:
        # 新建游标
        with db.cursor() as cursor:
            # 执行sql语句
            sql = "select * from user_info where employeeId = '{0}'".format(eid)
            cursor.execute(sql)
            # 取第一条
            data = cursor.fetchone()
            return data
    finally:
        db.close()
