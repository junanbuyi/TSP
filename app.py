
from flask import Flask, render_template, request, session, jsonify
from register import submit
from sign_up import login1
from user_register import register1
from user_waybill import submit_waybill
from v import view_waybill
from departure import departure_car
from RFM import *
import sys
import os
# 将 my_package 目录添加到 Python 的系统路径中
sys.path.append(os.path.abspath('D:\pycharm project\tsp1\notice'))
sys.path.append(os.path.abspath('D:\pycharm project\tsp1\map'))
sys.path.append(os.path.abspath('D:\pycharm project\tsp1\car'))
sys.path.append(os.path.abspath('D:\pycharm project\tsp1\machine_learning_model'))
from machine_learning_model.svm import svm1, svm2
from machine_learning_model.box import box1, box2
from car.car_arrival import index
from notice.see import notices
from notice.markdown import save_markdown_handler
from map.view import get_waybill_info


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qinxin'

#管理注册页面路由
@app.route('/')
def login():
    return render_template('login.html')

#处理管理注册信息路由
@app.route('/submit', methods=['POST'])
def sub():
    return submit()

#处理管理登录页面路由
@app.route('/admin')
def Admin():
    return render_template('submit.html')

#处理管理登录页面数据路由
@app.route('/admin1', methods=['POST'])
def Admin1():
    return login1()

#管理主页面路由
@app.route('/home')
def Home():
    return render_template('home.html')

#website,首页路由
@app.route('/website')
def site():
    return render_template('website.html')

#用户登陆页面路由
@app.route('/user_register')
def user_register():
    return  render_template('login1.html')

#用户登陆页面数据处理路由
@app.route('/user_register1', methods=['POST'])
def user_register1():
    return register1()

#处理管理登录页面路由
@app.route('/user_admin')
def user_admin():
    return render_template('submit1.html')

#处理管理登录页面数据路由
@app.route('/user_admin1', methods=['POST'])
def user_admin1():
    return login1()

#用户登录进入页面的路由
@app.route('/user_home')
def user_home():
    return render_template('user_goods.html')

#用户订单管理信息处理路由
@app.route('/api/waybill', methods=['POST'])
def api_waybill():
    return submit_waybill()

#用户订单创立之后支付路由
@app.route('/pay')
def pay():
    return render_template('pay.html')

#运单管理路由
@app.route('/waybill')
def manage():
    return render_template('goods.html')

#打印订单路由
@app.route('/waybill1')
def a():
    return view_waybill()

#拿取管理运单编号查询传输数据路由
@app.route('/administrater_waybill', methods=['POST','GET'])
def c():
    return view_waybill()

# 发车管理
@app.route('/departure')
def b():
    return render_template('car.html')

#接收出车表单信息的路由
@app.route('/car', methods=['POST'])
def e():
    return departure_car()

#地图显示
@app.route('/map_display')
def map_display():
    return render_template('map_display.html')

#车辆信息页面路由
@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html')

#财务分析路由
@app.route('/finance')
def goods_finance():
    return render_template('economic.html')
#RFM模型
@app.route('/rfm')
def r():
    rfm_analysis()
    return rfm_table()

#后端公告路由
@app.route('/notices')
def get_notices():
    notices_data = notices()
    return jsonify(notices_data)

#mackdown编写公告html渲染路由
@app.route('/mark')
def markdown():
    return render_template('markdown.html')

#定义保存Markdown内容的API接口
@app.route('/api/markdown', methods=['POST'])
def ma():
    return save_markdown_handler()

# 传回出发和到达位置，显示路由
@app.route('/view_waybill', methods=['POST'])
def view():
    return get_waybill_info()
#用户首页
@app.route('/user')
def user():
    return render_template('user_home.html')

# 到达页面
@app.route('/arrival')
def arrive():
    return index()

# svm
@app.route('/svm')
def svm():
    svm1()
    return svm2()
@app.route('/box')
def box():
    box1()
    return box2()
if __name__ == '__main__':
    app.run()
