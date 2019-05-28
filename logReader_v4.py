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

def viewableLog(name, zhibiao):
    df_industry=pd.read_csv('./data4/trade50.log')
    df_sub1 = df_industry[['2011-04-26','万方发展','90.1344688111111','4.4325','综合']]

    df_sub2 = df_sub1[(df_sub1["万方发展"] == name)]
    df_sub2.to_csv("./data5/"  + str(zhibiao).split('.')[0]+ name +".csv",encoding="utf-8", index=False)

if __name__ == "__main__":
    chicang, hangye_count = restoreReader()
    name_list = list(chicang.keys())
    for item in name_list:
        viewableLog(industry_dic[item][0], (chicang[item]['当前成本'] - chicang[item]['当前价格'])*chicang[item]['持仓数量'])