import baostock as bs
import pandas as pd
import time

def get_bao_PE(sltDate = '2019-03-24'):
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
            "进度:%3.2f%% | Code:%s | End@:%s | date:%s" % (100*jingduCount/len(rsAll.data), code, 
            time.asctime( time.localtime(newt+(newt - startt)/jingduCount*(len(rsAll.data) - jingduCount))),sltDate),end='   ')

        rs = bs.query_history_k_data_plus(str(code),
            "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
            start_date=sltDate, end_date=sltDate, 
            frequency="d", adjustflag="2")
        #### 打印结果集 ####
        if newt - startt > 9 and len(result_list) == 0:
            raise Exception('no PE data on it')

        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            lrs = rs.get_row_data()
            if(len(lrs) > 3 and lrs[3] != '' 
                        and float(lrs[3]) > 1e-3):
                result_list.append(lrs)
                break
        
    if len(result_list) == 0:
        raise Exception('no PE data on it')
    
    result = pd.DataFrame(result_list, columns=rs.fields)

    code_dic = {}
    for item in result.values:
        code_dic[item[1]] = float(item[3])
    bs.logout()
    return code_dic
    # #### 结果集输出到csv文件 ####
    # result.to_csv("./data2/read_PE_"+sltDate+".csv", encoding="utf-8", index=False)
    # #### 登出系统 ####

def get_bao_PE_byCode(code, sltDateBegin, sltDateEnd):
    lg = bs.login()
    rs = bs.query_history_k_data_plus(str(code),
        "date,code,peTTM",
        start_date=sltDateBegin, end_date=sltDateEnd, 
        frequency="d", adjustflag="2")
    result_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        lrs = rs.get_row_data()
        if lrs[2] != '' and float(lrs[2]) > -100:
            result_list.append(lrs)
            
    
    if len(result_list) == 0:
        raise Exception('no PE data on it')
    
    result = pd.DataFrame(result_list, columns=rs.fields)

    return result
    
if __name__ == "__main__":
    
    get_bao_PE()