#coding:utf-8
import json
import matplotlib.pyplot as plt
from pylab import * 
import pandas as pd
from choiceStockV4_debug import restoreReader, hangyeRead
industry_dic = hangyeRead()

def hangyeRead():
    df_industry=pd.read_csv('./data/stock_industry.csv')
    df_industry = df_industry[['code','code_name','industry']]
    industry_dic = {}
    for item in df_industry.values:
        industry_dic[item[0]] = item[1:3]

    return industry_dic

def viewableLog(name, zhibiao, hangye):
    df_industry=pd.read_csv('./data4/trade.log')
    df_sub1 = df_industry[[\
    '2011-04-26','股票具体名称','价格','指标','ROE','roe','PE','pe','板块'\
    ]]

    df_sub2 = df_sub1[(df_sub1["股票具体名称"] == name)]
    df_sub2.to_csv("./data5/"  + str(zhibiao).split('.')[0]+ name + '_'+ hangye +".csv",encoding="utf-8", index=False)

if __name__ == "__main__":
    chicang, hangye_count = restoreReader()
    print(chicang)
    name_list = list(chicang.keys())
    for item in name_list:
        viewableLog(industry_dic[item][0], (chicang[item]['当前成本'] - chicang[item]['当前价格'])*chicang[item]['持仓数量'], industry_dic[item][1])