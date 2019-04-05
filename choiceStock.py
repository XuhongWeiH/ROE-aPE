from bao_PE import get_bao_PE
import pandas as pd 
from datetime import datetime, timedelta
from tqdm import tqdm
import json

def daysAgo(inDate, days):
    oneyearago = datetime.strptime(inDate, '%Y-%m-%d') - timedelta(days=days)
    oneyearago = oneyearago.strftime('%Y-%m-%d')
    return oneyearago

def readROE(sltDate):
    df=pd.read_csv('./data3/dupont_data_ROE_(2015, 2020).csv')
    df = df[['code','pubDate','statDate','dupontROE']]\
        [(df["pubDate"] < sltDate) 
        & (daysAgo(sltDate, 455) < df["pubDate"])
        & (df["dupontROE"] > -1e6)
        ]

    df = df.sort_values(by='pubDate',ascending = False )
    code_dic = {}
    count_dic = {}
    for roe_item in tqdm(df.values):
        try:
            if count_dic[roe_item[0]] < 14:
                count_dic[roe_item[0]] += 1
                code_dic [roe_item[0]] += roe_item[3]
                pass
        except KeyError as identifier:
            count_dic[roe_item[0]] = 1
            code_dic [roe_item[0]] = roe_item[3]
            pass
    
    for k in count_dic.keys():
        code_dic[k] = code_dic[k] / count_dic[k] * 100
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
if __name__ == '__main__':
    sltDate = '2019-03-31'
    # readROE(sltDate)
    code_dic = readPE(sltDate)
    print(1)