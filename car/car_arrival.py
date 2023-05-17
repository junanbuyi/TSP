from flask import Flask, render_template, request
from database import Database
conn = Database()


def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 13

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM waybills")
    total_pages = 20

    cursor.execute("SELECT waybill_id, username, receiver FROM waybills LIMIT %s OFFSET %s", (per_page, (page-1)*per_page))
    waybills = cursor.fetchall()

    data = []
    for waybill in waybills:
        data.append({
            'id': waybill["waybill_id"],
            'name': waybill["username"],
            'address': waybill["receiver"]
        })

    return render_template('arrival.html', data=data, page=page, total_pages=total_pages)

