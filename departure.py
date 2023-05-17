from flask import request, jsonify
import uuid
from database import Database

def departure_car():
    # 获取表单数据
    departure_id = request.form.get('departure_id')
    departure_time = request.form.get('departure_time')
    driver_name = request.form.get('driver_name')
    driver_phone = request.form.get('driver_phone')
    license_plate = request.form.get('license_plate')

    # 生成唯一的运单编号
    waybill_id = str(uuid.uuid4())

    conn = Database()
    # 定义数据库表结构
    with conn.cursor() as cursor:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS car (id INT(11) NOT NULL AUTO_INCREMENT, waybill_id VARCHAR(255), driver_name VARCHAR(255), driver_phone VARCHAR(255), license_plate VARCHAR(255), departure_id VARCHAR(255), departure_time VARCHAR(255), PRIMARY KEY (id))')
        conn.commit()

    # 将数据存入数据库
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO car (waybill_id, driver_name, driver_phone, license_plate, departure_id, departure_time) VALUES (%s, %s, %s, %s, %s, %s)',
            (waybill_id, driver_name, driver_phone, license_plate, departure_id, departure_time))
        conn.commit()

    return jsonify({"message": "Success"}), 200
