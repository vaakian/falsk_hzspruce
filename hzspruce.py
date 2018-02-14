#coding=utf-8
import requests
from bs4 import BeautifulSoup
def get_cookies(usr, pas):
	log_url = 'http://pay.hzspruce.com/login_check.php'
	log_data = {
	'username' : usr,
	'password' : pas,
	'query' : ''
	}
	rsp = requests.post(log_url, data = log_data)
	log_cookies = rsp.cookies
	if(rsp.text == 'fai'):
		return 0
	else:
		print rsp.cookies
		return rsp.cookies
def get_html(usr, pas, url):
	username = usr
	password = pas
	log_cookies = get_cookies(username, password)
	if log_cookies:
		userinfo_page = requests.get(url, cookies = log_cookies)
		return userinfo_page.text
	else:
		return 0
def get_endtime(usr, pas):
	log_url = 'http://pay.hzspruce.com/userinfo.php'
	rsp = get_html(usr, pas, log_url)
	if(rsp):
		soup = BeautifulSoup(rsp, 'html.parser')
		select = '.co-blue-1'
		text = soup.select(select)
		text = handle(str(text[3]))
		return text
	else:
		return 0
def handle(text):
	text = text.replace('<td class="co-blue-1">', '')
	text = text.replace(' ', '')
	text = text.replace('</td>', '')
	text = text.replace('\n', '')
	temp = text
	text = ''
	for i in range(10):
		text = text + temp[i]
	text = text + ' '
	for j in range(10, 18):
		text = text + temp[j]
	return text
def get_order(usr, pas):
	order_url = 'http://pay.hzspruce.com/orderinfo.php'
	text = get_html(usr, pas, order_url)
	if(text):
		soup = BeautifulSoup(text, 'html.parser')
		text = soup.select('.order-content')
		return text
def handle_order(text):
	text = text.replace('<div class="order-content" style="display: none;">','')
	text = text.replace('<b>','')
	text = text.replace('</b>','')
	text = text.replace('<p>','')
	text = text.replace('</font> </p>','')
	text = text.replace('/div', '')
	text = text.replace('<font color="#519A01">', '')
	text = text.replace('<br/>', '')
	text = text.replace('<>', '')
	text = text.replace(' ', '')
	text = text.replace('详细信息'.decode('utf-8'), '')
	return text
def handleNone(text):
	return str(text).replace('none', 'inline')
def recharge(username, productID):
	url = 'http://pay.hzspruce.com/yueorderadd_check.php'
	data = {
	'username':username,
	'productID':productID,
	'productprice':'0.00'
	}
	rsp = requests.post(url, data = data)
	return (rsp.text).decode('utf-8')
def scanner_bak():
    url = 'http://pay.hzspruce.com/async.php?getproductprice='
    data={}
    for i in range(2,40):
        rsp = requests.get(url+str(i))
        data[i]=(rsp.text.encode("gbk"))
    return data
def wifi_reg(phonenum, password, vcode):
	url = 'http://pay.hzspruce.com/async.php'
	data = {
	'userreg':'yes',
	'mobile':phonenum,
	'names':'John',
	'vcode':vcode,
	'password':password,
	'projectID':'2',
	'query':''
	}
	rsp = requests.post(url, data = data)
	if rsp.text == 'suc':
		return 1
	return 0
def get_vcode(phonenum):
	url = 'http://pay.hzspruce.com/async.php?getregcode=' + phonenum
	rsp = requests.get(url)
	if rsp.text == 'suc':
		return 1
	return rsp.text