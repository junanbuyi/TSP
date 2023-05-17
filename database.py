import pymysql
def Database():
    # 定义数据库连接信息
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '753852941qx@',
        'db': 'tsp',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    # 连接数据库
    conn = pymysql.connect(**db_config)
    return conn
