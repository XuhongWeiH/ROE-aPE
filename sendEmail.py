import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import json
import pandas as pd
from datetime import datetime, timedelta
def daysAgo(inDate, days):
    oneyearago = datetime.strptime(inDate, '%Y-%m-%d') - timedelta(days=days)
    oneyearago = oneyearago.strftime('%Y-%m-%d')
    return oneyearago

def hangyeRead():
    df_industry=pd.read_csv('./data/stock_industry.csv')
    df_industry = df_industry[['code','code_name','industry']]
    industry_dic = {}
    for item in df_industry.values:
        industry_dic[item[0]] = item[1:3]

    return industry_dic

def getSTR():
    with open('./data2/out.json', 'r') as f:
        trade_list = json.load(fp=f)

    localtime = time.strftime("%Y-%m-%d", time.localtime())
    industry_dic = hangyeRead()
    send = []
    outStr = "代码 , 收盘日期 , 收盘价格 , 明日预测买卖方向 , 指标（越大越好), 股票名字, 所属板块\n"
    for item in trade_list:
        if daysAgo(localtime, 0) == item[1]:
            item += [industry_dic[item[0]][0], industry_dic[item[0]][1]]
            outStr += str(item)
            outStr += '\n' 
    outStr += "注意事项：\n \
                1.上午最佳卖出是早上开盘一冲高和11：00左右 (大盘高开10点前卖，低开等反弹在卖)。\n\
                2.上午最佳买入是大盘低开和10：00-10：30分左右。\n\
                3.下午最佳买入是2：00-2：30大家注意观察。\n\
                4.下午最佳卖出是13：10分-13：30分。\n\
                一定把我的这个邮箱设置为联系人，否则会进入到垃圾箱\
              "
    return outStr

def email(dstEmail, outStr):
    sender = '814123206@qq.com'
    localtime = time.strftime("%Y-%m-%d", time.localtime())
    smtp = smtplib.SMTP() 
    smtp.connect('smtp.qq.com',25) 
    smtp.login(sender, 'cyntatcmjvojbbdj') 

    msg=MIMEText(outStr,'plain','utf-8')
    msg['From']=formataddr(['魏旭鸿',sender])
    msg['To']=formataddr([dstEmail,dstEmail])
    msg['Subject']='在' + daysAgo(localtime, -1) + 'Asotck的操作'

    smtp.sendmail(sender, dstEmail, msg.as_string()) 
    smtp.quit()


if __name__ == "__main__":
    outStr = \
    '''
    操作内容,持仓在2/4,操作日期,2019-05-20,股票名称,韶钢松山,股票代码,sz.000717 \n
    操作内容,持仓在2/4,操作日期,2019-05-20,股票名称,华菱钢铁,股票代码,sz.000932 \n
    操作内容,持仓在3/4,操作日期,2019-05-20,股票名称,上峰水泥,股票代码,sz.000672 \n
    操作内容,持仓在2/4,操作日期,2019-05-20,股票名称,方大集团,股票代码,sz.000055 \n
    操作内容,清仓在0/4,操作日期,2019-05-20,股票名称,宜宾纸业,股票代码,sh.600793 \n
    操作内容,持仓在3/4,操作日期,2019-05-20,股票名称,方大炭素,股票代码,sh.600516 \n
    操作内容,持仓在2/4,操作日期,2019-05-20,股票名称,攀钢钒钛,股票代码,sz.000629 \n
    操作内容,持仓在2/4,操作日期,2019-05-20,股票名称,山鹰纸业,股票代码,sh.600567 \n

    比如土豪买每个股票都是3w,3w买的，那么他的满仓就是4/4，同理半仓就是代表他目前花了1.5w去买了股票x，
    像我的每个股票满仓就在1w附近，那么我的3/4仓就是7500左右

    05-20结束进行预测，操作内容为05-21的操作内容。仓位代表了05-21应该达到的水平。

    程序改版，以上内容仅供参考。如若购买了相同股票，可参照计算所得成比例改动自己的仓位。
    感谢朋友们支持，提出宝贵意见。由于新改版，所以程序处于不稳定状态。以上内容为操作前后两部分，请大家耐心观看，并对照20日结果，评价本次预测结果。
    '''
    sendlist = ['big_weixuhong@qq.com','719253612@qq.com','sunyixin610@126.com','364141009@qq.com','whitekreuz@163.com',\
                'zzhisheng@outlook.com']
    print(outStr)
    for item in sendlist:
        email(item, outStr)
        print(item, '   go')
    # try:
        
    # except as e :
        # print(e)
        # print('send failed', item)