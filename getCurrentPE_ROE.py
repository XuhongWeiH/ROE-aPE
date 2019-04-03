import requests
from bs4 import BeautifulSoup
import traceback
import re



def getHTMLText(url, code="utf-8"):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'}
    try:
        
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
    
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, "GB2312")
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue
        
def getStockInfo(lst, stockURL, fpath):
    Listtitle=['名称','总市值','净资产','净利润','市盈率','市净率','毛利率','净利率','ROE']
    with open(fpath,'w',encoding='utf-8') as f:
        for i in range(len(Listtitle)):
            f.write("{0:<10},".format(Listtitle[i],chr(12288)))
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url, "GB2312")
        try:
            if html=="":
                continue
            List=[]
            soup = BeautifulSoup(html, 'html.parser')
            stock = soup.find('div',attrs={'class':'cwzb'}).find_all('tbody')[0]
            name=stock.find_all('b')[0]
            List.append(name.text)
            keyList = stock.find_all('td')[1:9]
            for i in range(len(keyList)):
                List.append(keyList[i].text)
            with open(fpath,'a',encoding='utf-8') as f:
                f.write('\n')
                for i in range(len(List)):
                    f.write('{0:<10},'.format(List[i],chr(12288)))
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
            continue

def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'http://quote.eastmoney.com/'
    output_file = './Stock.txt'
    slist=[]
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()
