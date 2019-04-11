from bao_PE import get_bao_PE
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import json
from baoK_line import askPrice as _askPrice

def askPrice(code, date):
    try:
        price = _askPrice(code, date)
        return price #0.5 * (price[3] + price[4])
    except ValueError:
        price = askPrice(code, daysAgo(date,1))
        return price

def daysAgo(inDate, days):
    oneyearago = datetime.strptime(inDate, '%Y-%m-%d') - timedelta(days=days)
    oneyearago = oneyearago.strftime('%Y-%m-%d')
    return oneyearago

def readROE(sltDate):
    try:
        with open('./data2/ROE_' + sltDate + '.json', 'r') as f:
            code_dic = json.load(fp=f)
        pass
    except FileNotFoundError:
        df_origin=pd.read_csv('./data2/dupont_data_ROE_(2015, 2020).csv')
        df = df[['code','pubDate','statDate','dupontROE']]\
            [(df["pubDate"] < sltDate) 
            & (df["dupontROE"] > -1e6)
            ]

        # df = df.sort_values(by='pubDate',ascending = False )
        code_dic = {}
        count_dic = {}
        for roe_item in tqdm(df.values):
            try:
                if count_dic[roe_item[0]] < 4:
                    count_dic[roe_item[0]] += 1
                    code_dic [roe_item[0]] += roe_item[3]
                    pass
            except KeyError as identifier:
                count_dic[roe_item[0]] = 1
                code_dic [roe_item[0]] = roe_item[3]
                pass
        
        for k in count_dic.keys():
            if count_dic[k] >= 3:
                code_dic[k] = code_dic[k] / count_dic[k] * 100
            else:
                code_dic[k] = -1e6


        with open('./data2/ROE_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass
    return code_dic

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
        with open('./data2/PE_' + sltDate + '.json', 'r') as f:
            code_dic = json.load(fp=f)
        pass
    except FileNotFoundError:
        code_dic = _readPENewest(sltDate)
        with open('./data2/PE_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass
    return code_dic

def select_code(roe_dic_now, roe_dic_1_ago, roe_dic_2_ago, pe_dic, a=-98.3):
    select_code_dic = {}
    for k in pe_dic.keys():
        if 'ST' in k:
            continue
        try:
            if k == 'sh.600585':
                A = roe_dic_now[k]
                b = roe_dic_1_ago[k]
                c = roe_dic_2_ago[k]
                d = pe_dic[k]
            if roe_dic_now[k] >= 13 and roe_dic_1_ago[k] >= 10 and roe_dic_2_ago[k] >= 10 \
                and pe_dic[k] > 5:
                select_code_dic[k] = (roe_dic_now[k] + a*pe_dic[k],
                                        roe_dic_now[k],
                                        pe_dic[k],
                                        roe_dic_1_ago[k],
                                        roe_dic_2_ago[k])

            pass
        except KeyError:
            pass
    result = sorted(select_code_dic.items(), key=lambda e:e[1][0], reverse=True)
    return result

if __name__ == '__main__':
    sltDate = '2019-04-02'
    roe_dic_now = readROE(sltDate)
    roe_dic_1_ago = readROE(daysAgo(sltDate,365))
    roe_dic_2_ago = readROE(daysAgo(sltDate,365*2))
    pe_dic = readPE(sltDate)

    select_code(roe_dic_now, roe_dic_1_ago, roe_dic_2_ago, pe_dic)
    price = askPrice("sh.600230", "2019-04-08")
    print(1)
