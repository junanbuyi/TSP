from database import Database
import datetime
import json

def notices():
    # 连接数据库
    conn = Database()
    cursor = conn.cursor()
    # 查询最新的10条公告
    cursor.execute('SELECT content FROM markdown ORDER BY id DESC LIMIT 10')
    notices = cursor.fetchall()
    notices_str = json.dumps(notices)
    notices_dict = json.loads(notices_str)
    # 格式化公告的时间戳
    h = list()
    for i in range(len(notices_dict)):
        h.append(notices_dict[i]["content"])
    return h
