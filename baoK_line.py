import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
# print('login respond error_code:'+lg.error_code)
# print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data_plus("sh.600000",
    "date, code, open, high, low, close, isST",
    start_date='2017-07-01', end_date='2017-07-03',
    frequency="d", adjustflag="1")
# print('query_history_k_data_plus respond error_code:'+rs.error_code)
# print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())


#### 结果集输出到csv文件 ####   
# result.to_csv("./data3/history_A_stock_k_data.csv", index=False)
print(result)

#### 登出系统 ####
bs.logout()