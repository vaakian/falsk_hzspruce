import MySQLdb
def add_users(db, username, password):
	cursor = db.cursor()
	order = "INSERT INTO users SET username='" + username + "',password='" + password + "';"
	print order
	try:
		cursor.execute(order)
		data = cursor.fetchone()
		return 1
	except Exception as e:
		return 0

def check_users(db, username, password):
	cursor = db.cursor()
	order = "SELECT password FROM users WHERE username='"+username+"';"
	print order
	try:
		cursor.execute(order)
		password_corr = cursor.fetchone()[0]
		print password_corr
		if password == password_corr:
			return 1
		return 0
	except Exception as e:
		return 0
def select_chance(db, username):
	cursor = db.cursor()
	order = "SELECT chance FROM users WHERE username='"+username+"';"
	print order
	try:
		cursor.execute(order)
		chance = cursor.fetchone()[0]
		return chance
	except Exception as e:
		return 0
# if(check_users(db, 'admin', 'admin2')):
# 	print 'yes'
# else:
# 	print 'fail'
def reduce_chance(db, username):
	cursor = db.cursor()
	order = "UPDATE users SET chance=chance-1 WHERE username='"+username+"';"
	print order
	try:
		cursor.execute(order)
		chance = cursor.fetchone()[0]
		return chance
	except Exception as e:
		return 0
def mod_pass(db, username, password , to_password):
	if (username=='' or password == '' or to_password == ''):
		return 0
	cursor = db.cursor()
	order = "SELECT password FROM users WHERE username='"+username+"';"
	print order
	try:
		cursor.execute(order)
		password_corr = cursor.fetchone()[0]
		print password_corr
		if password == password_corr:
			try:
				order = "UPDATE users SET password = '"+ to_password +"' WHERE username='"+username+"';"
				cursor.execute(order)
				rsp = cursor.fetchone()
				return 1
			except Exception as e:
				return 0
		return 0
	except Exception as e:
		return 0
def add_chance(db, username, chance):
	cursor = db.cursor()
	order = "UPDATE users SET chance=chance+"+ str(chance) +" WHERE username='"+username+"';"
	print order
	try:
		cursor.execute(order)
		rsp = cursor.fetchone()
		print rsp
		return 1
	except Exception as e:
		return 0
def exe(db, order):
	cursor = db.cursor()
	print order
	try:
		cursor.execute(order)
		rsp = cursor.fetchall()
		cursor.close()
		return rsp
	except Exception as e:
		return 0
def del_user(db, username):
	cursor = db.cursor()
	order = "DELETE FROM users WHERE username='"+username+"';"
	print order
	try:
		cursor.execute(order)
		data = cursor.fetchone()
		return 1
	except Exception as e:
		return 0
if __name__ == '__main__':
	db = MySQLdb.connect('127.0.0.1','root','miniserver','john')
	exe(db, 'SELECT * FROM `users`')
