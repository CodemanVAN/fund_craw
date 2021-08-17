import requests
import json
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
def sendem(fund_details,receivers):
	
	#qq邮箱smtp服务器
	host_server = 'smtp.qq.com'
	#sender_qq为发件人的qq号码
	sender_qq = '@qq.com'
	#pwd为qq邮箱的授权码
	pwd = '' 
	sender_qq_mail = '@qq.com'
	
	#邮件的正文内容
	mail_content = fund_details
	#邮件标题
	st=requests.get('http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title='+time.strftime("%Y-%m-%d", time.localtime())).text
	st=json.loads(st)
	mail_title = st['content']+' '+st['note']
	#ssl登录
	smtp = SMTP_SSL(host_server)
	#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
	smtp.set_debuglevel(1)
	smtp.ehlo(host_server)
	smtp.login(sender_qq, pwd)

	msg = MIMEText(mail_content, "plain", 'utf-8')
	msg["Subject"] = Header(mail_title, 'utf-8')
	msg["From"] = sender_qq_mail
	
	for i in receivers:
		receiver = i
		msg["To"] = receiver
		smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
	smtp.quit()

fund_codes=['005825','002611','001717','540010','161725']

users=['@qq.com','@qq.com','@qq.com']
 


while(1):
	if (time.localtime().tm_hour ==14 ) and (time.localtime().tm_wday <5):
		msg='''*************************
			         每日基金播报
			*************************
			'''
		for i in fund_codes:
			url='http://fundgz.1234567.com.cn/js/'+i+'.js?rt=1463558676006'
			rsp=requests.get(url)
			res=json.loads(rsp.text[8:-2])
			msg+=res['name']+'\n--开盘价格为: '+res['dwjz']+'\n--当前价格为: '+res['gsz']+'\n--涨跌幅为: '+res['gszzl']+'%\n--时间为: '+res['gztime']+'\n*************************\n'
		sendem(msg,users)
		time.sleep(12*3600)


