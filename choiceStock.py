from bao_PE import get_bao_PE
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import json
from baoK_line import askPrice as _askPrice
import csv

para1 = 0.5
para2 = 0.3
para3 = -8.3

roe_lim_1 = 14
roe_lim_2 = 14

market_in_thread = -50
market_out_thread = -60
def askPrice(code, date):
    try:
        price = _askPrice(code, date)
        price[3] = float(price[3])
        price[4] = float(price[4])
        return price #0.5 * (price[3] + price[4])
    except ValueError:
        price = askPrice(code, daysAgo(date,1))
        price[3] = float(price[3])
        price[4] = float(price[4])
        return price

def daysAgo(inDate, days):
    oneyearago = datetime.strptime(inDate, '%Y-%m-%d') - timedelta(days=days)
    oneyearago = oneyearago.strftime('%Y-%m-%d')
    return oneyearago

def readROE(sltDate):
    try:
        with open('./data3/ROE_' + sltDate + '.json', 'r') as f:
            code_dic = json.load(fp=f)
        pass
    except FileNotFoundError:
        dateQujian = ['05-01','09-01','11-01']
        nowyear = sltDate.split('-')[0]
        nowmonth = '-'.join(sltDate.split('-')[1:])

        if nowmonth < dateQujian[0]:
            ago1Year = [int(nowyear)-1, 3]
            ago2Year = [int(nowyear)-2, 4]
            ago3Year = [int(nowyear)-3, 4]
        elif nowmonth < dateQujian[1]:
            ago1Year = [int(nowyear), 1]
            ago2Year = [int(nowyear)-1, 4]
            ago3Year = [int(nowyear)-2, 4]
        elif nowmonth < dateQujian[2]:
            ago1Year = [int(nowyear), 2]
            ago2Year = [int(nowyear)-1, 4]
            ago3Year = [int(nowyear)-2, 4]
        else:
            ago1Year = [int(nowyear), 3]
            ago2Year = [int(nowyear)-1, 4]
            ago3Year = [int(nowyear)-2, 4]       

        df_origin=pd.read_csv('./data/ROE_[2006, 2020].csv')
        df = df_origin[['code','pubDate','statDate', 'dupontROE', 'season', 'year']]\
            [(df_origin["pubDate"] < sltDate)
            &(daysAgo(sltDate,4*365+90) < df_origin["pubDate"] ) 
            ]

        df_ago1Year = df[(df['year']==ago1Year[0]) & (df['season']==ago1Year[1])]
        df_ago2Year = df[(df['year']==ago2Year[0]) & (df['season']==ago2Year[1])]
        df_ago3Year = df[(df['year']==ago3Year[0]) & (df['season']==ago3Year[1])]

        
        # df = df.sort_values(by='pubDate',ascending = False )
        code_dic = {}
        count_dic = {}
        for roe_item in tqdm(df_ago1Year.values):
            try:
                count_dic[roe_item[0]] += 1
                code_dic [roe_item[0]] += [roe_item[3]*100/roe_item[4]*4]

            except KeyError as identifier:
                count_dic[roe_item[0]] = 1
                code_dic [roe_item[0]] = [roe_item[3]*100/roe_item[4]*4]
                pass

        for roe_item in tqdm(df_ago2Year.values):
            try:
                count_dic[roe_item[0]] += 1
                code_dic [roe_item[0]] += [roe_item[3]*100/roe_item[4]*4]

            except KeyError as identifier:
                count_dic[roe_item[0]] = 1
                code_dic [roe_item[0]] = [roe_item[3]*100/roe_item[4]*4]
                pass

        for roe_item in tqdm(df_ago3Year.values):
            try:
                count_dic[roe_item[0]] += 1
                code_dic [roe_item[0]] += [roe_item[3]*100/roe_item[4]*4]

            except KeyError as identifier:
                count_dic[roe_item[0]] = 1
                code_dic [roe_item[0]] = [roe_item[3]*100/roe_item[4]*4]
                pass
        
        for k in count_dic.keys():
            if count_dic[k] < 3:
                code_dic.pop(k)

        with open('./data3/ROE_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass
    
    new_code_dic = {}
    for k in code_dic.keys():
        if code_dic[k][1] > roe_lim_1 and code_dic[k][2] > roe_lim_2:
            new_code_dic[k] = code_dic[k][0] + para1*code_dic[k][1] + para2*code_dic[k][2]
            new_code_dic[k] /=3
    return new_code_dic

def _readPENewest(sltDate):
    try:
        pe_result = get_bao_PE(sltDate)
        pass
    except Exception:
        last_sltDate = daysAgo(sltDate,1)
        pe_result = _readPENewest(last_sltDate)

    return pe_result

def readPE(sltDate):
    try:
        with open('./data3/PE_' + sltDate + '.json', 'r') as f:
            code_dic = json.load(fp=f)
        pass
    except FileNotFoundError:
        code_dic = _readPENewest(sltDate)
        with open('./data3/PE_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass
    return code_dic

def select_code(roe_dic, pe_dic):
    select_code_dic = {}
    for k in pe_dic.keys():
        if 'ST' in k:
            continue
        try:

            if pe_dic[k] > 5:
                select_code_dic[k] = (roe_dic[k] + para3*pe_dic[k],
                                        roe_dic[k],
                                        pe_dic[k],
                                        )

            pass
        except KeyError:
            pass
    result = sorted(select_code_dic.items(), key=lambda e:e[1][0], reverse=True)
    return result, select_code_dic

def exchange(sltDate, result, shizhi_chenben, select_code_dic, out, industry_dic):

    #设定写入模式
    # out += [['code', 'date', 'price', 'direction','zhibiao']]
    market_quality = 0
    for r in result:
        if r[1][0] > market_in_thread:
            market_quality += 1
    result_small = result[:market_quality]

    new_shizhi_chenben = {}
    hangye_count = {}
    for r in result_small:
        try:
            if hangye_count[industry_dic[r[0]][1]] > 0:
                continue
            hangye_count[industry_dic[r[0]][1]] += 1
            pass
        except KeyError:
            hangye_count[industry_dic[r[0]][1]] = 1
            pass
            
        if r[0] in shizhi_chenben.keys():
            new_shizhi_chenben[r[0]] = shizhi_chenben[r[0]]
            continue
        else:
            price = askPrice(r[0], sltDate)
            price = (price[3] + price[4])/2
            new_shizhi_chenben[r[0]] = (industry_dic[r[0]][0], price, r[1][0], industry_dic[r[0]][1])
            out += [[r[0], sltDate, price, 'buy', r[1][0]]]

    sold_list = []
    for k in shizhi_chenben.keys():
        if select_code_dic[k][0] < market_out_thread:
            sold_list = sold_list + [k]
            price = askPrice(k, sltDate)
            price = (price[3] + price[4])/2
            out += [[k, sltDate, price, 'sold', select_code_dic[k][0] ]]

    for delt_item in sold_list:
        new_shizhi_chenben.pop(delt_item)
    
    return new_shizhi_chenben

def hangyeRead():
    df_industry=pd.read_csv('./data/stock_industry.csv')
    df_industry = df_industry[['code','code_name','industry']]
    industry_dic = {}
    for item in df_industry.values:
        industry_dic[item[0]] = item[1:3]

    return industry_dic


if __name__ == '__main__':
    shizhi_chenben = {}
    ziben = 100000
    sltDate = '2016-05-13'
    industry_dic = hangyeRead()
    #打开文件，追加a
    out = []
    while sltDate < '2019-04-03':
        sltDate = daysAgo(sltDate,-15)

        roe_dic = readROE(sltDate)
        pe_dic = readPE(sltDate)
        result, select_code_dic = select_code(roe_dic, pe_dic)
        shizhi_chenben = exchange(sltDate, result, shizhi_chenben, select_code_dic, out, industry_dic)
    
    print(1)
