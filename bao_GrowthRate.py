import baostock as bs
import pandas as pd
import time
import json
from datetime import datetime, timedelta

def GrowthRate(sltDate_years_ago, sltDate):
    lg = bs.login()
    rsAll = bs.query_stock_basic ()
    jingduCount = 0
    startt = time.time()

    result_list = []
    while (rsAll.error_code == '0') & rsAll.next():
        # 获取一条记录，将记录合并在一起
        code = rsAll.get_row_data()[0]
        jingduCount += 1
        newt = time.time()
        
        
        print('\r',
            "进度:%3.2f%% | Code:%s | End@:%s | date:%s" % (100*jingduCount/len(rsAll.data), code, 
            time.asctime( time.localtime(newt+(newt - startt)/jingduCount*(len(rsAll.data) - jingduCount))),sltDate),end='   ')

        rs = bs.query_performance_express_report(code, start_date=sltDate_years_ago, end_date=sltDate)
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
            
    result = pd.DataFrame(result_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####
    code_dic = {}
    for item in result.values:
        try:
            code_dic[item[0]] = code_dic[item[0]]
        except KeyError:
            code_dic[item[0]] = float(item[6])*100

    return code_dic

def readG(sltDate_years_ago, sltDate):
    try:
        with open('./data3/G_' + sltDate + '.json', 'r') as f:
            code_dic = json.load(fp=f)
        pass
    except FileNotFoundError:
        
        code_dic = GrowthRate(sltDate_years_ago, sltDate)

        with open('./data3/G_' + sltDate + '.json', 'w') as f:
            json.dump(code_dic, f)
        pass
    return code_dic
if __name__ == "__main__":
    readG('2018-12-01', '2019-06-01')

