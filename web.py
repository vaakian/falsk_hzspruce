#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask,render_template,jsonify,session,redirect
from flask import request
from flask_admin import Admin, BaseView, expose, AdminIndexView
from hzspruce import *
from users import *
db = MySQLdb.connect("127.0.0.1","root","miniserver","john")
# db = MySQLdb.connect('sql12.freemysqlhosting.net','sql12221089','YvkeMzMDHc','sql12221089')
app = Flask(__name__)
app.secret_key = u'johnkiller'
admin = Admin(app,name = u"John's Tools for Web",index_view=AdminIndexView(
        name='导航',
        template='welcome.html',
        url='/tools'
    ))
# class Admin(BaseView):ss
# 	@expose('/',methods=['GET'])
# 	def tools(self):
# 		if 'username' in session:
# 			return self.render('welcome.html',message='logined')
# 		return redirect('../login')
class seek(BaseView):
	@expose('/',methods=['GET'])
	def index(self):
		if 'username' in session:
			return self.render('seek.html')
		return self.render('logout.html', notlog=True)
	@expose('/',methods=['POST'])
	def index2(self):
		endtime = taocan = username = alert = ''
		global endtime, taocan, username , alert
		username = request.form['username']
		password = request.form['password']
		if(username and password):
			endtime = get_endtime(username, password)
			if(endtime):
				taocan = []
				taocan_temp = list(get_order(username, password))
				if(len(taocan_temp)):
					for i in taocan_temp:
						taocan.append(handleNone(i))
					print "Current usr:"+username
					taocan = taocan
					endtime = endtime
					username = username
				else:
					alert = username + '未激活！'
			else:
				alert = '账号或密码错误！'
		else:
			alert = '账号或密码不为空！'
		return self.render('seek.html', endtime = endtime, taocan = taocan, username = username, alert = alert)
class charge(BaseView):
	@expose('/', methods=['GET'])
	def index(self):
		if 'username' in session:
			return self.render('recharge.html', session_user = session['username'])
		return self.render('logout.html', notlog=True)
	@expose('/', methods=['POST'])
	def index_post(self):
		username = request.form['username']
		productID = request.form['productID']
		if(select_chance(db, session['username'])>0):
			rsp_t = recharge(username,productID)
			if rsp_t == 'suc':
				reduce_chance(db, session['username'])
		else:
			rsp_t='chanceerr'
		return rsp_t
	@expose('/own/', methods=['GET'])
	def index_own(self):
		return self.render('recharge_own.html')
	@expose('/own/', methods=['POST'])
	def index_own_post(self):
		username = request.form['username']
		productID = request.form['productID']
		rsp_t = recharge(username,productID)
		if rsp_t == 'suc':
			reduce_chance(db, session['username'])
		return rsp_t
class reg(BaseView):
	@expose('/')
	def reg_index(self):
		if 'username' in session:
			return self.render('reg.html')
		return self.render('logout.html', notlog=True)
	@expose('/', methods=['POST'])
	def reg(self):
		phonenum = password = vcode = rsp = alert = ''
		global phonenum, password, vcode, rsp, alert
		phonenum = request.form['phonenum']
		password = request.form['password']
		vcode = request.form['vcode']
		rsp = wifi_reg(phonenum, password, vcode)
		if (rsp):
			reduce_chance(db, session['username'])
			return 'suc'
		else:
			return 'fai'
	@expose('/get_vcode', methods=['GET'])
	def function(self):
		return '404 not found.',404
	@expose('/get_vcode', methods=['POST'])
	def get_vcode(self):
		phonenum = request.form['phonenum']
		global phonenum, password
		if (len(phonenum) == 11):
			rsp = get_vcode(phonenum)
			if rsp==1:
				return 'suc'
				# rsp = phonenum + '已经获取验证码，请查收。'
			else:
				return 'alredy'
				# rsp = phonenum + '已注册，请直接登录。'
		else:
			return 'err'
			# rsp = '请输入正确的手机号！'
#		return self.render('reg.html', alert = rsp, phonenum = phonenum, password = password)
class logout(BaseView):
	@expose('/')
	def logout(self):
		if 'username' in session:
			session.pop('username')
		if '_login' in session:
			session.pop('_login')
   		return self.render('logout.html', logout=True)
#上面只是一个class 需要 add_view(class_name)
class profile(BaseView):
	@expose('/')
	def profile(self):
		if 'username' in session:
			return self.render('profile.html',username = session['username'], chance = select_chance(db,session['username']))
		return redirect('/login')
	@expose('/add',methods=['POST', 'GET'])
	def addchance(self):
		if request.method == 'POST':
			username = request.form['username']
			chance = request.form['chance']
			message = ''
			if(add_chance(db, username, chance)):
				message = u'充值成功'
			return self.render('addchance.html',message = message)
		return self.render('addchance.html')
	@expose('/users',methods=['POST','GET'])
	def users(self):
		users = exe(db, 'SELECT * FROM `users`')
		return self.render('users.html',users = users)
	@expose('/del',methods=['GET'])
	def del_(self):
		username = request.args.get("username")
		print username
		del_user(db, username)
		return redirect('/tools/profile/users')
class modpass(BaseView):
	@expose('/',methods=['GET','POST'])
	def modpass(self):
		if 'username' in session:
			if request.method == 'POST':
				username = request.form['username']
				password = request.form['password']
				to_password = request.form['to_password']
				if(mod_pass(db, username, password, to_password)):
					message = u'修改成功，新密码为：' + to_password + u',请妥善保管！'
				else:
					message = u'修改失败'
				return self.render('modpass.html',message = message)
			return self.render('modpass.html')
		return redirect('/login')
class reguser(BaseView):
	@expose('/', methods=['POST', 'GET'])
	def reguser(self):
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			if session['username'] == 'admin':
				if(add_users(db, username, password)):
					return 'suc'
				return 'fail'
			return 'erruser'
		if 'username' in session:
			return self.render('reg_john.html')
		return redirect('/login')
admin.add_view(seek(name = u'订单查询',category = 'WiFi工具'))
admin.add_view(charge(name = u'WiFi充值', category = 'WiFi工具'))
admin.add_view(reg(name= u'WiFi账号注册', category ='WiFi工具'))

admin.add_view(profile(name=u'个人资料', category = u'个人中心'))
admin.add_view(modpass(name=u'修改密码', category = u'个人中心'))
admin.add_view(reguser(name=u'Sign In', category = u'个人中心'))
admin.add_view(logout(name=u'LogOut', category = u'个人中心'))
@app.route('/')
def home():
	if 'username' in session:
		return redirect('/tools/profile')
	return redirect('../login')
@app.route('/login',methods=['POST','GET'])
def login():
	if request.method =='POST':
		username = request.form['username']
		password = request.form['password']
		if(check_users(db, username, password)):
			session['username'] = username
			session['_login'] = True
			return 'suc'
		return 'fail'
	return render_template('login.html')
@app.errorhandler(404)
def page_not_found(e):
	if 'username' in session:
   		return redirect('/tools/profile')
   	return redirect('/login')
app.run(port=800,debug=True,host='0.0.0.0',threaded=True)