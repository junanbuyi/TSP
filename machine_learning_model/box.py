
from database import Database
from flask import render_template
def box1():
    # 连接数据库
    conn = Database()
    cursor = conn.cursor()

    # 查询每个客户的运输次数、货物种类、货物重量、货物金额等信息
    query = """SELECT username, COUNT(*) AS waybill_count, COUNT(DISTINCT cargo_type) AS cargo_type_count,
       SUM(cargo_weight) AS total_weight
        FROM waybills
        GROUP BY username"""
    cursor.execute(query)

    # 存储RFM指标
    rfm_scores = []
    for row in cursor.fetchall():
        username, waybill_count, cargo_type_count, total_weight = row
        r_score = float(row[waybill_count])  # R: 最近一次交易时间
        f_score = float(row[cargo_type_count])  # F: 交易频率
        m_score = float(row[total_weight])  # M: 交易金额
        rfm_score = int(100 * r_score + 10 * f_score + 1 * m_score)
        rfm_scores.append((username, rfm_score))

        # 根据RFM指标判断优质客户
        if rfm_score >= 211 and rfm_score < 311:
            customer_type = "高价值客户"
        elif rfm_score >= 111 and rfm_score < 211:
            customer_type = "重点保持客户"
        elif rfm_score >= 311:
            customer_type = "重点发展客户"
        else:
            customer_type = "一般客户"

        with conn.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS customer_rfm_score (
                customer_name VARCHAR(255) NOT NULL,
                r_score INT NOT NULL,
                f_score INT NOT NULL,
                m_score INT NOT NULL,
                rfm_score INT NOT NULL,
                customer_type VARCHAR(255) NOT NULL,
                PRIMARY KEY (customer_name)
            )"""
            cursor.execute(create_table_query)
            # 将计算结果插入到数据库中
            insert_query = """INSERT INTO customer_rfm_score (customer_name, r_score, f_score, m_score, rfm_score, customer_type)
                              VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (row[username], r_score, f_score, m_score, rfm_score, customer_type))

            conn.commit()


def box2():
    # 连接数据库
    conn = Database()
    cursor = conn.cursor()

    # 查询客户RFM信息
    query = """SELECT customer_name, r_score, f_score, m_score, rfm_score, customer_type
                FROM customer_rfm_score"""
    cursor.execute(query)

    # 将查询结果保存到一个列表中
    customers = []
    for row in cursor.fetchall():
        customer = {
            "name": row["customer_name"],
            "r_score": row["r_score"],
            "f_score": row["f_score"],
            "m_score": row["m_score"],
            "rfm_score": row["rfm_score"],
            "customer_type": row["customer_type"]
        }
        customers.append(customer)
    cursor.execute("""DROP table customer_rfm_score""")
    # 渲染页面并将数据传递给前端
    return render_template("box.html", customers=customers)