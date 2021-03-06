#--*--coding: utf-8--*--

from flask import Flask                   # 从flask包导入Flask类
from flask import request                 # 从flask包导入request对象
from flask import session                 # 从flask包导入session对象 
from flask import redirect                # 从flask包导入redirect函数
from flask import render_template         # 从flask包导入render_template函数 

from common import authentication
from common import register
from common import get_user
from common import get_users 
from common import userDel 
from common import userInfo
from common import userEdit
from common import rname

from auth import login_required


import json
import logging
#import logging.handlers 







app = Flask(__name__)
app.secret_key = 'oF\xd3I\x98\xe5\xb4\x1a\xfb\xc77\xe3\xcc,\xc2\xd2\x05\x8b\xa9\x9b\x01\xa0t\x0f\x04\x11\x19\xcd4\x96\x8d\x14'


'''首页
'''
@app.route('/')
@login_required
def index():
    logging.debug('index')
    return render_template('index.html')


'''登录
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug('login')
    #print request.form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #if authentication(username, password):
        authinfo,ok = authentication(username, password)
        if ok:
            session['sign'] = username
            return redirect("/")
        else:
            #errmsg = "InValid username or password"
            return render_template('login.html', errmsg=authinfo)
    else:
        return render_template('login.html')



@app.route('/checkusername', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def checkusername():
    logging.debug('')
    if request.method == 'POST':
        data = request.form.to_dict()
        #print data
        #print rname(data)
        if rname(data):
            return json.dumps({"status":0})
        else:
            return json.dumps({"status":1})
    else:
        return redirect("/users")


'''用户
'''
@app.route('/users', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def users():
    logging.debug('')
    search_value = request.args.get("search")
    if request.method == 'POST':
        data = request.form.to_dict()
        #if data['username'] and data['email'] and data['password']:
        response = register(data)
        #    return "11111111"
        #else:
        return json.dumps({"status":1})
    else:
        if search_value:
            users = get_user(search_value) 
        else:
            users = get_users()
        return render_template('users.html', users=users)
'''
@app.route('/users', methods=['GET', 'POST', 'DELETE', 'PUT'])
def users():
    search_value = request.args.get("search")
    if search_value:
        users = get_user(search_value) 
    else:
        users = get_users()
    return render_template('users.html', users=users)
'''


'''用户删除
'''
@app.route('/users/<int:uid>', methods=['GET'])
@login_required
def usersDel(uid):
    logging.debug('')
    response = userDel(uid)
    return redirect('/users')

'''用户修改
'''
@app.route('/users/edit', methods=['POST','GET'])
@login_required
def usersedit():
    logging.debug('user eidt')
    if request.method == 'POST':
        data = request.form.to_dict()
        #print data
        user = userEdit(**data)
        return json.dumps({'status':0})
    else:
        return redirect('/users') 


'''用户添加
'''
@app.route('/users/add', methods=['GET', 'POST'])
@login_required
def users_add():
    logging.debug('user add')
    if request.method == 'POST':
        data = request.form.to_dict()
        if data['password'] != data['rpassword']:
            errmsg = "Confirm password error"
            return render_template('users_add.html', errmsg=errmsg)
        # 1. 判断用户是否存在，用户存在，提示改用户已被注册

        # 2. 判断邮箱的后缀是不是公司的邮箱后缀 @51reboot.com

        # 3. 密码复杂性要求 长度不能低于8位 必须包含大写、小写和特殊字符等

        print data
        response = register(data)
        print response

        return redirect("/users")
    else:
        return render_template('users_add.html')


'''资产
'''
@app.route('/assets')
def assets():
    return render_template('assets.html')


'''性能监控
'''
@app.route('/performance_monitor')
def performance_monitor():
    return render_template('monitor.html')


'''退出
'''
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')






if __name__ == '__main__':
    LOG_FILE = '/tmp/myapp.log'
    logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format='[%(asctime)s] - [%(threadName)5s] - [%(filename)s-line:%(lineno)d] [%(levelname)s] %(message)s'
            )
    logging.debug('started')
    app.run(host='0.0.0.0', port=9000, debug=True)
