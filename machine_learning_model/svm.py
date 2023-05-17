import numpy as np
from database import Database
from flask import render_template
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def svm_model():
    # 连接数据库
    conn = Database()
    cursor = conn.cursor()

    # 查询每个客户的运输次数、货物种类、货物重量、货物金额等信息
    query = """SELECT username, COUNT(*) AS waybill_count, COUNT(DISTINCT cargo_type) AS cargo_type_count,
       SUM(cargo_weight) AS total_weight
        FROM waybills
        GROUP BY username"""
    cursor.execute(query)

    # 存储RFM指标和标签
    features = []
    labels = []
    for row in cursor.fetchall():
        waybill_count = float(row['waybill_count'])
        cargo_type_count = float(row['cargo_type_count'])
        total_weight = float(row['total_weight'])

        rfm_score = [waybill_count, cargo_type_count, total_weight]
        features.append(rfm_score)

        # 根据RFM指标判断客户类型
        if rfm_score[0] >= 211 and rfm_score[0] < 311:
            customer_type = "高价值客户"
        elif rfm_score[0] >= 111 and rfm_score[0] < 211:
            customer_type = "重点保持客户"
        elif rfm_score[0] >= 311:
            customer_type = "重点发展客户"
        else:
            customer_type = "一般客户"
        labels.append(customer_type)

    # 将标签转换为数值
    label_mapping = {"高价值客户": 0, "重点保持客户": 1, "重点发展客户": 2, "一般客户": 3}
    labels = [label_mapping[label] for label in labels]

    # Ensure there are at least two classes in the dataset
    unique_classes = set(labels)
    if len(unique_classes) < 2:
        raise ValueError("The dataset should contain at least two classes for SVM classification.")

    # 数据清洗：用中位数填充缺失值或空值
    features = np.array(features)
    median_values = np.nanmedian(features, axis=0)
    features = np.where(np.isnan(features), median_values, features)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # 创建SVM模型并训练
    svm_model = SVC()
    svm_model.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = svm_model.predict(X_test)

    # 计算模型性能指标
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # 渲染页面并将数据传递给前端
    return render_template("svm.html", accuracy=accuracy, precision=precision, recall=recall, f1=f1)


def svm1():
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


def svm2():
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
    return render_template("svm.html", customers=customers)


