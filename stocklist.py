# coding:utf-8
import re
import urllib.request
stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'

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
