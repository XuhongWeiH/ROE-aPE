from bao_PE import get_bao_PE
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import json
from baoK_line import askPrice as _askPrice
import csv
import logging
import numpy as np
import math
from bao_tradeDay import isTradeDay
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='./data4/trade.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logging.info('持仓,操作日期,2011-04-26,股票名称,股票具体名称,当前价格,价格,今日指标,指标,ROE,roe,PE,pe,所属板块,板块')
def hangyeRead():
    df_industry=pd.read_csv('./data/stock_industry.csv')
    df_industry = df_industry[['code','code_name','industry']]
    industry_dic = {}
    for item in df_industry.values:
        industry_dic[item[0]] = item[1:3]

    return industry_dic
industry_dic = hangyeRead()

para0 = 1
para1 = 0.8
para2 = 0.6
para3 = -3.3

roe_lim_1 = 20
roe_lim_2 = 20

market_in_thread = 0#

zongzichan = 100000
zichantouru = 0
geguzijingjishu = zongzichan * 0.1#

cangwei_feature_step = 10000000.1#
cangwei_real_step = 0.0

hangye_max = 100

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

def askCodePrice(code, date):
    price = askPrice(code, date)
    priceValue = (price[3] + price[4])/2
    return priceValue

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

        # debug
        with open('./data3/ROE_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass
    
    new_code_dic = {}
    chicang, hangye_count = restoreReader()
    for k in code_dic.keys():
        if code_dic[k][1] > roe_lim_1 and code_dic[k][2] > roe_lim_2 or k in chicang.keys():
            new_code_dic[k] = para0*code_dic[k][0] + para1*code_dic[k][1] + para2*code_dic[k][2]
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
        # debug
        with open('./data3/PE_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass 
    return code_dic

def partition(L_key, L_value, left, right):
    """
    将L[left:right]进行一次快速排序的partition，返回分割点
    :param L: 数据List
    :param left: 排序起始位置
    :param right: 排序终止位置
    :return: 分割点
    """
    if left < right:
        key = L_value[left]
        key_tmp = L_key[left]
        low = left
        high = right
        while low < high:
            while low < high and L_value[high][0] <= key[0]:
                high = high - 1
            L_value[low] = L_value[high]
            L_key[low] = L_key[high]
            while low < high and L_value[low][0] >= key[0]:
                low = low + 1
            L_value[high] = L_value[low]
            L_key[high] = L_key[low]
        L_value[low] = key
        L_key[low] = key_tmp
    return low

def topK(L_key, L_value, K):
    """
    求L中的前K个最小值
    :param L: 数据List
    :param K: 最小值的数目
    """
    if len(L_key) < K:
        pass
    low = 0
    high = len(L_key) - 1
    j = partition(L_key, L_value, low, high)
    while j != K: # 划分位置不是K则继续处理
        if K > j: #k在分划点后面部分
            low = j + 1
        else:
            high = j           # K在分划点前面部分
        j = partition(L_key, L_value, low, high)
    return L_key[:K], L_value[:K]

def dic2list(select_code_dic):
    list_keys = list(select_code_dic.keys())
    list_values = []
    for item in list_keys:
        list_values += [select_code_dic[item]]

    return list_keys, list_values

def select_code(roe_dic, pe_dic):
    select_code_dic = {}
    
    for k in list(roe_dic.keys()) + list(pe_dic.keys()):
        try:
            if 'ST' in industry_dic[k][0]:
                select_code_dic[k] = (-1000,
                                        0,
                                        0,
                                        )
                continue
        except KeyError:
            select_code_dic[k] = (-1001,
                                        0,
                                        0,
                                        )
            continue
        try:
            if roe_dic[k] > -100 and pe_dic[k] > -1:
                select_code_dic[k] = (roe_dic[k] + para3*pe_dic[k],
                                            roe_dic[k],
                                            pe_dic[k],
                                            )
            else:
                raise(KeyError)
        except KeyError:
            select_code_dic[k] = (-1002,
                                        0,
                                        0,
                                        )
            pass
    list_keys, list_values = dic2list(select_code_dic)
    list_keys_topk, list_values_topk = topK(list_keys, list_values, 50)
    select_code_dic_sub_sorted = {}
    for item_k in range(len(list_keys_topk)):
        select_code_dic_sub_sorted[list_keys_topk[item_k]] = list_values_topk[item_k]
    result = sorted(select_code_dic_sub_sorted.items(), key=lambda e:e[1][0], reverse=True)
    return result, select_code_dic

def storeSaver(chicang,hangye):
    with open('./data4/chicang.json', 'w') as f:
        json.dump(chicang, f)
    with open('./data4/hangye.json', 'w') as f:
        json.dump(hangye, f)
    
def restoreReader():
    chicang_dic = {}
    hangye_count = {}
    try:
        with open('./data4/chicang.json', 'r') as f:
            chicang_dic = json.load(fp=f)
    except FileNotFoundError:
        print('./data4/chicang.json is not exit')
        return chicang_dic, hangye_count
        pass

    try:
        with open('./data4/hangye.json', 'r') as f:
            hangye_count = json.load(fp=f)
    except FileNotFoundError:
        print('./data4/hangye.json is not exit')
        return chicang_dic, hangye_count
        pass
    
    return chicang_dic, hangye_count

def buyAnalyse(sltDate, result, select_code_dic):

    global zongzichan
    global geguzijingjishu
    global zichantouru
    chicang, hangye_count = restoreReader()
    market_quality = 0
    for r in result:
        if r[1][0] > market_in_thread:
            market_quality += 1
    result_small = result[:market_quality]

    for r in result_small:
        if (r[0] in chicang.keys() and chicang[r[0]]['仓位状态'] > 0) or \
            industry_dic[r[0]][1] == '钢铁'or \
            industry_dic[r[0]][1] == '化工'or \
            industry_dic[r[0]][1] == '机械设备'or \
            industry_dic[r[0]][1] == '传媒'or \
            industry_dic[r[0]][1] == '公事业'or \
            industry_dic[r[0]][1] == '汽车'or \
            industry_dic[r[0]][1] == '综合'or \
            industry_dic[r[0]][1] == '建筑装饰'or \
            industry_dic[r[0]][1] == '医药生物' or \
            r[1][2] < 5 or \
            r[1][2] > 11:# or r[1][0] > 30 :
            #  or len(chicang.keys()) >= 15 or zichantouru > zongzichan*0.8:
            continue
        # if r[0] != 'sh.601166':
        #     continue
        else:
            try:
                if hangye_count[industry_dic[r[0]][1]] > hangye_max:
                    continue
                hangye_count[industry_dic[r[0]][1]] += 1
                pass
            except KeyError:
                hangye_count[industry_dic[r[0]][1]] = 1
                pass

            price = askCodePrice(r[0], daysAgo(sltDate,-1))
            stock_buy = max(0.5*geguzijingjishu/price//100*100,200)
            chicang[r[0]] = {
                            '操作日期': daysAgo(sltDate,-1),
                            '股票名称': industry_dic[r[0]][0],
                            '股票代码': r[0],
                            '指标初始': r[1][0],
                            '今日指标': r[1][0],
                            'ROE': r[1][1],
                            'PE': r[1][2],
                            '当前成本': price,
                            '当前价格': price,
                            '持仓数量': stock_buy,
                            '单位操作': 100*math.ceil(stock_buy/200),
                            '仓位状态': 0.5,
                            '资金投入': stock_buy*price,
                            '所属板块': industry_dic[r[0]][1]
            }
            zichantouru = 0
            for item in chicang.keys():
                zichantouru += chicang[item]['持仓数量'] * chicang[item]['当前成本']

            # logging.debug(','.join(['明日操作', '建仓',
            #                        '操作日期', daysAgo(sltDate,-1),
            #                        '股票名称', industry_dic[r[0]][0],
            #                        '股票代码', r[0],
            #                        '指标初始', str(r[1][0]),
            #                        '今日指标', str(r[1][0]),
            #                        '当前成本', str(price),
            #                        '当前价格', str(price),
            #                        '持仓数量', str(stock_buy),
            #                        '单位操作', str(100 * (math.ceil(stock_buy/200))),
            #                        '仓位状态', str(0.5),
            #                        '资金投入', str(stock_buy*price),
            #                        '所属板块', industry_dic[r[0]][1]]))
    storeSaver(chicang, hangye_count)

    # chicang.pop(delt_item)
    
def holdAnalyse(sltDate, select_code_dic):

    global zongzichan
    global geguzijingjishu
    global zichantouru
    soldall_list = []
    chicang, hangye_count = restoreReader()
    for item in chicang.keys():
        try:
            new_feature = select_code_dic[item][0]
        except KeyError:
            print(item, '没有 指标信息')
            new_feature = -998

        chicang_tmp = chicang[item]
        last_feature = chicang_tmp['今日指标']
        origin_feature = chicang_tmp['指标初始']
        dinamic_cangwei = chicang_tmp['仓位状态']

        last_cangwei_tmp = abs(last_feature - origin_feature) // cangwei_feature_step * np.sign(last_feature - origin_feature)
        new_cangwei_tmp = abs(new_feature - origin_feature) // cangwei_feature_step * np.sign(new_feature - origin_feature)

        cangwei_det = (new_cangwei_tmp - last_cangwei_tmp) * cangwei_real_step
        zichantouru = 0
        for item_in in chicang.keys():
            zichantouru += chicang[item_in]['持仓数量'] * chicang[item_in]['当前成本']

        # if cangwei_det > 0 and zichantouru >= zongzichan:
        #     cangwei_det = 0
        #     new_feature = last_feature

        dinamic_cangwei = max(dinamic_cangwei + cangwei_det, 0)

        price_new = askCodePrice(item, daysAgo(sltDate,-1))

        if dinamic_cangwei == 0 or select_code_dic[item][0] == -1002 or select_code_dic[item][1] < 12:
            caozuoneirong = '清仓'
            print('清仓', select_code_dic[item], industry_dic[item][0], industry_dic[item][1])
            soldall_list += [item]
            hangye_count[industry_dic[item][1]] -= 1
            stock_buy_sell = -1*chicang_tmp['持仓数量']
        else:
            stock_buy_sell = chicang_tmp['单位操作'] * (dinamic_cangwei - chicang_tmp['仓位状态'])/0.25
            if cangwei_det > 0:
                caozuoneirong = '加仓'
            elif cangwei_det == 0:
                caozuoneirong = '持仓'
            elif cangwei_det < 0:
                caozuoneirong = '减仓'

        if (chicang_tmp['持仓数量'] + stock_buy_sell) == 0:
            dangqianchenben = (chicang_tmp['资金投入'] + stock_buy_sell*price_new)/100
        else:
            dangqianchenben = (chicang_tmp['资金投入'] + stock_buy_sell*price_new) / \
                                    (chicang_tmp['持仓数量'] + stock_buy_sell)
        chicang[item] = {'操作日期': daysAgo(sltDate,-1),
                        '股票名称': industry_dic[item][0],
                        '股票代码': item,
                        '指标初始': chicang_tmp['指标初始'],
                        '今日指标': new_feature,
                        'ROE': select_code_dic[item][1],
                        'PE': select_code_dic[item][2],
                        '当前成本': dangqianchenben,
                        '当前价格': price_new,
                        '持仓数量': chicang_tmp['持仓数量'] + stock_buy_sell,
                        '单位操作': chicang_tmp['单位操作'],
                        '仓位状态': dinamic_cangwei,
                        '资金投入': chicang_tmp['资金投入'] + stock_buy_sell*price_new,
                        '所属板块': industry_dic[item][1]
            }

        logging.info(','.join(['明日操作', caozuoneirong,
                                '操作日期', daysAgo(sltDate,-1),
                                '股票名称', industry_dic[item][0],
                                # '股票代码', item,
                                # '指标初始', str(chicang_tmp['指标初始']),
                                # '昨日指标', str(last_feature),#5
                                # '当前成本', str(chicang_tmp['当前成本']),#4
                                '当前价格', str(chicang_tmp['当前价格']),
                                # '持仓数量', str(chicang_tmp['持仓数量']),#1
                                # '仓位状态', str(chicang_tmp['仓位状态']),#2
                                # '资金投入', str(chicang_tmp['资金投入']),#3
                                # '单位操作', str(chicang_tmp['单位操作']),
                                # '持仓变至', str(chicang_tmp['持仓数量'] + stock_buy_sell),#1
                                # '仓位变至', str(dinamic_cangwei),#2
                                # '资金变至', str(chicang_tmp['资金投入'] + stock_buy_sell*price_new),#3
                                # '成本变至', str(dangqianchenben),#4
                                '今日指标', str(new_feature),
                                'ROE', str(select_code_dic[item][1]),
                                'PE', str(select_code_dic[item][2]),
                                '所属板块', industry_dic[item][1]]))
    
    for item in soldall_list:
        print('清仓了', item,industry_dic[item][0], chicang[item]['资金投入'])
        zongzichan -= chicang[item]['资金投入']
        chicang.pop(item)

    zichantouru = 0
    for item in chicang.keys():
        zichantouru += chicang[item]['持仓数量'] * chicang[item]['当前成本']

    print("总资产,总市值,持股数,%s---%.2f---%.2f---%d" %(sltDate, zongzichan, zichantouru,len(chicang.keys())))

    storeSaver(chicang, hangye_count)
    





if __name__ == '__main__':

    sltDate = '2007-03-12'
    
    while sltDate < '2009-05-29':#今日日期，预测明日
        sltDate = daysAgo(sltDate,-1)
        if not isTradeDay(sltDate):
            continue
        # roe_dic = readROE(sltDate)
        pe_dic = readPE(sltDate)
    #     result, select_code_dic = select_code(roe_dic, pe_dic)
    #     buyAnalyse(sltDate, result, select_code_dic)
    #     holdAnalyse(sltDate, select_code_dic)
    #     # , chicang, hangye_count
    # chicang, _ = restoreReader()
    # for item in chicang.keys():
    #     print('强制平仓了', item,industry_dic[item][0], (chicang[item]['当前成本'] - chicang[item]['当前价格'])*chicang[item]['持仓数量'])
    #     zongzichan -= (chicang[item]['当前成本'] - chicang[item]['当前价格'])*chicang[item]['持仓数量']
    #     print(zongzichan)
        
