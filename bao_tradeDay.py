import baostock as bs
import pandas as pd

def isTradeDay(sltDate):
    lg = bs.login()
    rs = bs.query_trade_dates(start_date="2017-01-01", end_date="2017-06-30")
    data_list = []
    while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    return bool(int(data_list[0][1]))