from bao_PE import get_bao_PE
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import json
from baoK_line import askPrice as _askPrice
import csv
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
 
logging.basicConfig(filename='trade.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
 
# logging.debug("This is a debug log.")
# logging.info("This is a info log.")
# logging.warning("This is a warning log.")
# logging.error("This is a error log.")
# logging.critical("This is a critical log."

para1 = 0.5
para2 = 0.3
para3 = -3.3

roe_lim_1 = 14
roe_lim_2 = 14

market_in_thread = -6.5

zongzihan = 100000
zijingzonge = zongzihan * 0.6
geguzijingjishu = zongzihan * 0.1

hangye_max = 1

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

def select_code(roe_dic, pe_dic, industry_dic):
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

            select_code_dic[k] = (roe_dic[k] + para3*pe_dic[k],
                                        roe_dic[k],
                                        pe_dic[k],
                                        )
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

def exchange(sltDate, result, chicang, select_code_dic, industry_dic, hangye_count):

    #设定写入模式
    # 获取符合指标范围的股票
    market_quality = 0
    for r in result:
        if r[1][0] > market_in_thread:
            market_quality += 1
    result_small = result[:market_quality]

    for r in result_small:
        if r[0] in chicang.keys() or r[1][0] > 30:
            continue
        else:
            try:
                if hangye_count[industry_dic[r[0]][1]] > hangye_max:
                    continue
                hangye_count[industry_dic[r[0]][1]] += 1
                pass
            except KeyError:
                hangye_count[industry_dic[r[0]][1]] = 1
                pass
            price = askCodePrice(r[0], sltDate)
            chicang[r[0]] = (industry_dic[r[0]][0], price, r[1][0], 0.5*geguzijingjishu/price//100*100,industry_dic[r[0]][1])
            logging.info(','.join(['操作日期', sltDate,
                                   '买入股票', industry_dic[r[0]][0],
                                   '股票代码', r[0],
                                   '指标数值', str(r[1][0]),
                                   '当前成本', str(price),
                                   '当前价格', str(price),
                                   '持仓数量', str(0.5*geguzijingjishu/price//100*100),
                                   '仓位状态', str(0.5),
                                   '所属板块', industry_dic[r[0]][1]]))
    return chicang, hangye_count

    # sold_list = []
    # for k in chicang.keys():
    #     try:
    #         if select_code_dic[k][0] < market_out_thread:
    #             sold_list = sold_list + [k]
    #             price = askCodePrice(k, sltDate)
    #             out += [[k, sltDate, price, 'sold', select_code_dic[k][0] ]]
    #     except KeyError:
    #         sold_list = sold_list + [k]
    #         price = askCodePrice(k, sltDate)
    #         out += [[k, sltDate, price, 'sold', 33366]]
    #         pass

    # for delt_item in sold_list:
    #     chicang.pop(delt_item)
    #     hangye_count[industry_dic[delt_item][1]] -= 1
    #     assert(hangye_count[industry_dic[delt_item][1]] > -1)

    # for item in chicang.keys():
    #     try:
    #         price = askCodePrice(item, sltDate)
    #         chicang[item] = (industry_dic[item][0], price, select_code_dic[item][0], industry_dic[item][1])
    #         price = askCodePrice(item, sltDate)
    #         out += [[item, sltDate, price, 'hold', select_code_dic[item][0]]]
    #     except KeyError:
    #         price = askCodePrice(item, sltDate)
    #         chicang[item] = (industry_dic[item][0], price, -100, industry_dic[item][1])
    #         price = askCodePrice(item, sltDate)
    #         out += [[item, sltDate, price, 'hold', -100]]
    
    
    # with open('./data2/out.json', 'w') as f:
    #     json.dump(out, f)    
        
    # return chicang, hangye_count


    

def hangyeRead():
    df_industry=pd.read_csv('./data/stock_industry.csv')
    df_industry = df_industry[['code','code_name','industry']]
    industry_dic = {}
    for item in df_industry.values:
        industry_dic[item[0]] = item[1:3]

    return industry_dic



if __name__ == '__main__':
    chicang = {}
    hangye_count = {}
    hangye_count['房地产'] = hangye_max+1
    hangye_count['银行'] = hangye_max+1
    sltDate = '2016-05-01'
    industry_dic = hangyeRead()
    
    while sltDate < '2019-04-30':#今日日期，预测明日
        sltDate = daysAgo(sltDate,-2)

        roe_dic = readROE(sltDate)
        pe_dic = readPE(sltDate)
        result, select_code_dic = select_code(roe_dic, pe_dic, industry_dic)
        chicang, hangye_count = exchange(sltDate, result, chicang, select_code_dic, industry_dic, hangye_count)
        for it in chicang.items():
            print(it)
        print(sltDate, ':', hangye_count)
    print(1)
