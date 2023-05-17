from flask import request
import hashlib
from database import Database
from flask import jsonify
def login1():
    # 获取表单数据
    username = request.form.get('username')
    password = request.form.get('password')

    conn = Database()
    # 从数据库中查找用户信息
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM user_1 WHERE username=%s', (username,))
        user = cursor.fetchone()

    # 验证用户名和密码是否匹配
    if user is not None and hashlib.sha256(password.encode()).hexdigest() == user['password']:
        # 用户名和密码匹配，登陆成功
        response = jsonify({"message": "Success"})
        response.status_code = 200
        response.set_cookie('username', username)  # 设置 cookie
        return response
    else:
        # 用户名和密码不匹配，登陆失败
        response = jsonify({"message": "Incorrect username or password"})
        response.status_code = 401
        return response
