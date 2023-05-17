from flask import request, jsonify
import uuid
from database import Database
# UUID模块生成唯一的运单编号

def submit_waybill():
    # 获取表单数据
    username = request.form.get('username')
    sender = request.form.get('sender')
    receiver = request.form.get('receiver')
    shipping_date = request.form.get('shippingDate')
    delivery_date = request.form.get('deliveryDate')
    cargo_type = request.form.get('cargoType')
    cargo_weight = request.form.get('cargoWeight')
    shipping_fee = request.form.get('shippingFee')
    is_delivered = request.form.get('isDelivered')

    # 生成唯一的运单编号
    waybill_id = str(uuid.uuid4())

    conn = Database()
    # 定义数据库表结构
    with conn.cursor() as cursor:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS waybills (id INT(11) NOT NULL AUTO_INCREMENT, username VARCHAR(255) , waybill_id VARCHAR(255), sender VARCHAR(255), receiver VARCHAR(255), shipping_date VARCHAR(255), delivery_date VARCHAR(255), cargo_type VARCHAR(255), cargo_weight INT(11), shipping_fee INT(11), is_delivered VARCHAR(255), PRIMARY KEY (id))')
        conn.commit()

    # 将数据存入数据库
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO waybills (username, waybill_id, sender, receiver, shipping_date, delivery_date, cargo_type, cargo_weight, shipping_fee, is_delivered) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (username, waybill_id, sender, receiver, shipping_date, delivery_date, cargo_type, cargo_weight, shipping_fee, is_delivered))
        conn.commit()


    return jsonify({"message": "Success", "waybill_id": waybill_id}), 200


