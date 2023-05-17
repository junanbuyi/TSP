from flask import request, jsonify
from database import Database
import requests


def get_location(address):
    # 高德地图Web服务API的URL
    url = "https://restapi.amap.com/v3/geocode/geo"
    # 高德地图开发者账号的API密钥
    api_key = 'c352d440bbda1826666caa9b73881186'
    # 构造请求参数
    params = {
        'key': api_key,
        'address': address
    }

    # 发送GET请求到高德地图API
    response = requests.get(url + '?key=' + api_key + '&address=' + address)
    print(response.text)  # 打印完整的请求 URL
    # 解析响应数据
    r = response.json()
    # 提取地理编码结果
    if r['status'] == '1' and int(r['count']) > 0:
        location = r['geocodes'][0]['location']
        return location.split(',')
    else:
        return None

def get_waybill_info():
    # 从请求中获取运单编号
    waybill = request.form['waybill']
    conn = Database()
    # 查询数据库表 waybill 中相应的出发和到达地点
    cursor = conn.cursor()
    cursor.execute("SELECT sender, receiver FROM waybills WHERE waybill_id = %s", (waybill,))
    result = cursor.fetchone()
    # 如果找到了相应的出发和到达地点，则将查询结果以 JSON 格式返回给前端
    if result:
        start_location = get_location(result['sender'])
        end_location = get_location(result['receiver'])
        print(start_location,end_location)
        if start_location and end_location:
            return jsonify({'start': start_location, 'end': end_location}), 200
        else:
            return jsonify({'error': 'Geocoding failed'}), 500
    # 否则返回 404 错误
    return jsonify({'error': 'Waybill not found'}), 404
