from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = '6789023yhfkjasd234'


@app.route('/login', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        flash('用户名或密码不正确')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
