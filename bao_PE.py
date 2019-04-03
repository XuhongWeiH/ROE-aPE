import baostock as bs
import pandas as pd
import time
#### 登陆系统 ####
def get_bao_PE(yearSE = '2019-03-24'):
    lg = bs.login()
    # 显示登陆返回信息
    # print('login respond error_code:'+lg.error_code)
    # print('login respond  error_msg:'+lg.error_msg)

    #### 获取沪深A股估值指标(日频)数据 ####
    # peTTM    滚动市盈率
    # psTTM    滚动市销率
    # pcfNcfTTM    滚动市现率
    # pbMRQ    市净率
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
            "进度:%.2f%% | Code:%s | End@:%s | date:%s" % (100*jingduCount/len(rsAll.data), code, 
            time.asctime( time.localtime(newt+(newt - startt)/jingduCount*(len(rsAll.data) - jingduCount))),yearSE),end='')


        rs = bs.query_history_k_data_plus(str(code),
            "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
            start_date=yearSE, end_date=yearSE, 
            frequency="d", adjustflag="1")
        #### 打印结果集 ####

        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            lrs = rs.get_row_data()
            if(len(lrs) > 3 and lrs[3] != '' 
                        and float(lrs[3]) > 0.000001):
                result_list.append(lrs)
                break
    if len(result_list) == 0:
        print('no PE data on ', yearSE)
        return 0
    result = pd.DataFrame(result_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("./data3/history_PE_"+yearSE+".csv", encoding="utf-8", index=False)
    #### 登出系统 ####
    bs.logout()
    return 1
if __name__ == "__main__":
    get_bao_PE()