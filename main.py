#-*- coding: UTF-8 -*-
from flask import Flask, request, redirect, render_template, make_response
from chat import chat_gpt2

app = Flask(__name__)

# 定义一个字典，用于保存已注册的用户的用户名和密码
users = {'admin1': '123456', 'admin2': '123456', 'admin3': '123456'}


@app.route('/')
def index():
    # 检查 cookie 中是否存在 username，如果存在则跳转至主页
    username = request.cookies.get('username')
    if username in users:
        return render_template('index.html', username=username)
    # 如果未登录则跳转至登录页
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果请求为 POST，则进行身份验证
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 检查用户名和密码是否正确
        if username in users and users[username] == password:
            # 如果验证通过，则在 cookie 中保存用户名
            response = make_response(redirect('/'))
            response.set_cookie('username', username)
            return response
        else:
            # 如果验证失败，则返回错误提示
            return render_template('login.html', error='Invalid username or password.')
    # 如果请求为 GET，则显示登录表单
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    # 删除 cookie 中的 username，并跳转至登录页
    response = make_response(redirect('/login'))
    response.delete_cookie('username')
    return response


@app.route('/quest', methods=['POST'])
def quest():
    # 检查 cookie 中是否存在 username，如果存在则跳转至主页
    username = request.cookies.get('username')
    if username in users:
        data = request.form.get("data")
        print("You:" + data)
        # generate_text()
        response = chat_gpt2(prompt=data, userID=username)
        print("Bot:" + response)
        return response
    # 如果未登录则跳转至登录页
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run()
