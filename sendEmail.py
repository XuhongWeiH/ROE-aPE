import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import json
def email(dstEmail):
    with open('./data2/out.json', 'r') as f:
        trade_list = json.load(fp=f)

    send = []
    outStr = "代码 , 操作日期 , 收盘价格 , 买卖方向 , 指标（越大越好）\n"
    for item in trade_list:
        outStr += str(item)
        outStr += '\n' 

    localtime = time.localtime(time.time())
    date = '-'.join([str(localtime[0]),str(localtime[1]),str(localtime[2])])
    smtp = smtplib.SMTP() 
    smtp.connect('smtp.163.com',25) 
    smtp.login('13122192187', 'w123123') 

    msg=MIMEText(outStr,'plain','utf-8')
    msg['From']=formataddr(['xhwei','13122192187@163.com'])
    msg['To']=formataddr([dstEmail,dstEmail])
    msg['Subject']=date + "明日股票买卖清单"

    smtp.sendmail('13122192187@163.com', dstEmail, msg.as_string()) 
    smtp.quit()

if __name__ == "__main__":
    email('814123206@qq.com')
    email('719253612@qq.com')
    # email('sunyixin610@126.com')