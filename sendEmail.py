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
    sh.600793 宜宾纸业 轻工制造
    sz.000672 上峰水泥 建筑材料
    sh.600516 方大炭素 有色金属
    sz.000629 攀钢钒钛 采掘
    sz.000537 广宇发展 房地产

    这个版本通过这段时间不断地在实际中磨合，以及和各种志同道合的胖友讨论，现在已进入稳定运行的阶段。\n
    算法后面我还会有大的更新，但是这一个版本能够预计达到15~20%的年化收益。\n
    上述列出的股票大家只需要买，尤其是在跌的时候，买入，千万不要因为蝇头小利给卖了，或是跌了一点就卖了。\n
    没有所谓的止盈点，除非出现更好的股票,或者在高估值的时候卖出，届时我会发邮件告诉大家。

    在该版本的正式运行阶段，如果没有邮件通知就是持有，如果有邮件通知，就是要买入新的低估值股票，以及卖出高估值的股票。\n
    上述股票为目前的基本组合，应用日期为2019-05-30，如果之前的邮件都没有跟上进度的话，明天就可以在适当的时候买入上述股票。
    '''
    outStr += "注意事项：\n \
                以上股票随便买，都是低估值，有钱就买，越便宜越买\
                1.上午最佳卖出是早上开盘一冲高和11：00左右 (大盘高开10点前卖，低开等反弹在卖)。\n\
                2.上午最佳买入是大盘低开和10：00-10：30分左右。\n\
                3.下午最佳买入是2：00-2：30大家注意观察。\n\
                4.下午最佳卖出是13：10分-13：30分。\n\
                \
              "
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