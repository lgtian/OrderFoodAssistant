from flask import Flask, request, render_template, redirect, url_for, Response
from service.user_service import query_user_pwd
from util.util import is_str_empty

app = Flask(__name__)
app.secret_key = '6789023yhfkjasd234'


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     return render_template('login.html')


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


if __name__ == '__main__':
    app.run(debug=True)
