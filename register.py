from flask import Flask, request
import hashlib
from database import Database
from flask import jsonify

def submit():
    # 获取表单数据
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    conn = Database()
    # 定义数据库表结构
    with conn.cursor() as cursor:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS users (id INT(11) NOT NULL AUTO_INCREMENT, username VARCHAR(50), email VARCHAR(50), password VARCHAR(255), PRIMARY KEY (id))')
        conn.commit()

    # 检查密码是否一致
    if password != confirm_password:
        return 'Password and confirm password do not match.'

    # 将密码进行哈希加密
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # 将数据存入数据库
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                       (username, email, hashed_password))
        conn.commit()
    return jsonify({"message": "Success"}), 200