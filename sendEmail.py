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
-------------------------------
 1- 1 成长25% 白云山 医药生物 利35亿 攻103.58% 防150.80%  现价34.67￥ 卖价80.14￥ 股息率1.22% pe=14.30 PEG=0.57
 1- 1白云山,建仓价格:34.67,-5%=32.94￥,-10%=31.20￥,建仓日期2019-08-09

 1- 2 成长26% 华东医药 医药生物 利23亿 攻94.06% 防111.90%  现价25.73￥ 卖价59.97￥ 股息率1.28% pe=17.90 PEG=0.68
 1- 2华东医药,建仓价格:25.73,-5%=24.44￥,-10%=23.16￥,建仓日期2019-08-09

 1- 3 成长33% 济川药业 医药生物 利16亿 攻106.27% 防102.22%  现价27.88￥ 卖价82.56￥ 股息率4.41% pe=13.12 PEG=0.40
 1- 3济川药业,建仓价格:27.88,-5%=26.49￥,-10%=25.09￥,建仓日期2019-08-09

 1- 4 成长20% 华兰生物 医药生物 利12亿 攻82.88% 防140.26%  现价30.04￥ 卖价53.08￥ 股息率1.33% pe=35.37 PEG=1.73
 1- 4华兰生物,建仓价格:30.04,-5%=28.54￥,-10%=27.04￥,建仓日期2019-08-09

-------------------------------
 2- 5 成长17% 保利地产 房地产 利261亿 攻99.06% 防112.85%  现价13.72￥ 卖价24.05￥ 股息率3.64% pe=7.17 PEG=0.41
 2- 5保利地产,建仓价格:13.72,-5%=13.03￥,-10%=12.35￥,建仓日期2019-08-09

 2- 6 成长27% 新城控股 房地产 利122亿 攻104.28% 防117.09%  现价24.55￥ 卖价68.10￥ 股息率6.11% pe=5.36 PEG=0.19
 2- 6新城控股,建仓价格:24.55,-5%=23.32￥,-10%=22.10￥,建仓日期2019-08-09

 2- 7 成长33% 金科股份 房地产 利40亿 攻103.60% 防134.17%  现价5.90￥ 卖价18.19￥ 股息率6.10% pe=7.94 PEG=0.24
 2- 7金科股份,建仓价格:5.9,-5%=5.61￥,-10%=5.31￥,建仓日期2019-08-09

-------------------------------
 3- 8 成长20% 贵州茅台 食品饮料 利378亿 攻69.95% 防124.44%  现价945.00￥ 卖价1622.04￥ 股息率1.54% pe=30.14 PEG=1.51
 3- 8贵州茅台,建仓价格:945.0,-5%=897.75￥,-10%=850.50￥,建仓日期2019-08-09

 3- 9 成长16% 洋河股份 食品饮料 利81亿 攻98.20% 防113.82%  现价105.58￥ 卖价175.17￥ 股息率3.03% pe=18.37 PEG=1.14
 3- 9洋河股份,建仓价格:105.58,-5%=100.30￥,-10%=95.02￥,建仓日期2019-08-09

 3-10 成长11% 伊利股份 食品饮料 利64亿 攻81.66% 防98.37%  现价28.16￥ 卖价38.48￥ 股息率2.49% pe=25.95 PEG=2.27
 3-10伊利股份,建仓价格:28.16,-5%=26.75￥,-10%=25.34￥,建仓日期2019-08-09

 3-11 成长27% 口子窖 食品饮料 利15亿 攻61.71% 防105.94%  现价58.74￥ 卖价128.33￥ 股息率2.55% pe=21.64 PEG=0.77
 3-11口子窖,建仓价格:58.74,-5%=55.80￥,-10%=52.87￥,建仓日期2019-08-09

 3-12 成长31% 涪陵榨菜 食品饮料 利6亿 攻102.55% 防151.59%  现价21.99￥ 卖价54.67￥ 股息率1.18% pe=25.86 PEG=0.82
 3-12涪陵榨菜,建仓价格:21.99,-5%=20.89￥,-10%=19.79￥,建仓日期2019-08-09

 3-13 成长12% 洽洽食品 食品饮料 利4亿 攻72.78% 防138.61%  现价25.97￥ 卖价34.91￥ 股息率1.93% pe=28.45 PEG=2.34
 3-13洽洽食品,建仓价格:25.97,-5%=24.67￥,-10%=23.37￥,建仓日期2019-08-09

 1- 1 成长12% 恒顺醋业 食品饮料 利3亿 攻60.64% 防137.34%  现价14.55￥ 卖价19.80￥ 股息率0.84% pe=35.08 PEG=2.88
 1- 1恒顺醋业,建仓价格:14.55,-5%=13.82￥,-10%=13.10￥,建仓日期2019-08-13
-------------------------------
 4-14 成长15% 宁沪高速 交通运输 利44亿 攻94.99% 防117.15%  现价10.27￥ 卖价16.34￥ 股息率4.48% pe=11.77 PEG=0.77
 4-14宁沪高速,建仓价格:10.27,-5%=9.76￥,-10%=9.24￥,建仓日期2019-08-09

 4-15 成长28% 粤高速A 交通运输 利19亿 攻103.06% 防113.90%  现价7.68￥ 卖价18.06￥ 股息率7.32% pe=9.50 PEG=0.34
 4-15粤高速A,建仓价格:7.68,-5%=7.30￥,-10%=6.91￥,建仓日期2019-08-09

-------------------------------
 5-16 成长25% 海大集团 农林牧渔 利14亿 攻76.75% 防129.34%  现价30.52￥ 卖价57.81￥ 股息率0.98% pe=31.94 PEG=1.27
 5-16海大集团,建仓价格:30.52,-5%=28.99￥,-10%=27.47￥,建仓日期2019-08-09

 5-17 成长25% 安琪酵母 农林牧渔 利8亿 攻76.71% 防99.79%  现价29.38￥ 卖价57.68￥ 股息率1.19% pe=29.66 PEG=1.17
 5-17安琪酵母,建仓价格:29.38,-5%=27.91￥,-10%=26.44￥,建仓日期2019-08-09

-------------------------------
 6-18 成长25% 中国平安 非银金融 利1204亿 攻66.20% 防119.65%  现价83.47￥ 卖价157.50￥ 股息率1.32% pe=2.55 PEG=0.10
 6-18中国平安,建仓价格:83.47,-5%=79.30￥,-10%=75.12￥,建仓日期2019-08-09

-------------------------------
 7-19 成长23% 中国国旅 休闲服务 利39亿 攻60.86% 防150.21%  现价86.20￥ 卖价158.76￥ 股息率0.64% pe=37.78 PEG=1.59
 7-19中国国旅,建仓价格:86.2,-5%=81.89￥,-10%=77.58￥,建仓日期2019-08-09

-------------------------------
 8-20 成长16% 格力电器 家用电器 利263亿 攻73.74% 防101.25%  现价50.27￥ 卖价80.86￥ 股息率2.98% pe=11.50 PEG=0.68
 8-20格力电器,建仓价格:50.27,-5%=47.76￥,-10%=45.24￥,建仓日期2019-08-09

 8-21 成长21% 苏泊尔 家用电器 利16亿 攻71.32% 防144.10%  现价66.50￥ 卖价115.50￥ 股息率1.53% pe=30.87 PEG=1.42
 8-21苏泊尔,建仓价格:66.5,-5%=63.17￥,-10%=59.85￥,建仓日期2019-08-09

-------------------------------
 9-22 成长10% 招商银行 银行 利808亿 攻69.44% 防122.88%  现价34.53￥ 卖价44.70￥ 股息率2.72% pe=1.64 PEG=0.16
 9-22招商银行,建仓价格:34.53,-5%=32.80￥,-10%=31.08￥,建仓日期2019-08-09

 9-23 成长18% 宁波银行 银行 利112亿 攻74.86% 防115.16%  现价22.10￥ 卖价36.59￥ 股息率1.81% pe=1.70 PEG=0.09
 9-23宁波银行,建仓价格:22.1,-5%=21.00￥,-10%=19.89￥,建仓日期2019-08-09

-------------------------------
10-24 成长15% 海螺水泥 建筑材料 利306亿 攻90.13% 防141.39%  现价38.26￥ 卖价69.60￥ 股息率4.42% pe=6.52 PEG=0.42
10-24海螺水泥,建仓价格:38.26,-5%=36.35￥,-10%=34.43￥,建仓日期2019-08-09
'''
    outStr = """注意事项：\n \
建仓价格参考
""" \
              + outStr

    sendlist = ['big_weixuhong@qq.com']
    # , 'qiujtmaric@163.com','719253612@qq.com'\
    # ,'sunyixin610@126.com','364141009@qq.com','whitekreuz@163.com',\
    #            'zzhisheng@outlook.com','chenyf_sh@163.com', 'zhao129363@163.com','675988851@qq.com','1173289264@qq.com',\
    # '756670951@qq.com','maric_downyxu@163.com'           ]
    print(outStr)
    for item in sendlist:
        email(item, outStr)
        print(item, '   go')
    # try:
        
    # except as e :
        # print(e)
        # print('send failed', item)