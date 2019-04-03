# coding:utf-8
import re
import urllib.request
import csv

def downback(a,c):
   ''''
   a:已经下载的数据
   c:远程文件的大小
  '''
   per = 100.0 * a / c
   if per > 100 :
       per = 100
   print('%.2f%%' % per)
stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
#获取股票代码列表

def urlTolist(url):
    allCodeList = []
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0]=='6' or item[0]=='3' or item[0]=='0':
            allCodeList.append(item)
    return allCodeList

allCodelist = urlTolist(stock_CodeUrl)

count_num = 0
for code in allCodelist:
    count_num += 1
    print('正在获取%s股票数据...'%code)
    if code[0]=='6':
        url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
        '&end=20191231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    else:
        url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+\
        '&end=20191231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

    # writer.writerow(("日期",'开盘价','最高价','最低价','收盘价','涨跌额','涨跌幅','成交量','成交金额','振幅','换手率'))
    urllib.request.urlretrieve(url,'./data2/'+code+'.csv')#可以加一个参数dowmback显示下载进度
    downback(count_num, len(allCodelist))
