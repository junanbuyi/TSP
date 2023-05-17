from flask import render_template
from database import Database
from flask import request

def view_waybill():
    conn = Database()
    waybill_id = request.form.get('waybill-id')
    print(waybill_id)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM waybills WHERE waybill_id = %s', (waybill_id,))
        waybill_data = cursor.fetchone()
        print(waybill_data)
    if waybill_data:
        # 如果查询到了运单数据，则将数据渲染到waybill.html模板中
        return render_template('waybill.html', waybill_data=waybill_data)
    else:
        # 如果没有查询到运单数据，则返回404错误页面
        return '未找到该运单', 404

