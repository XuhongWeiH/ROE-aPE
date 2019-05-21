import baostock as bs
import pandas as pd

def isTradeDay(sltDate):
    lg = bs.login()
    rs = bs.query_trade_dates(start_date=sltDate, end_date=sltDate)
    data_list = []
    while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    bs.logout()
    return bool(int(data_list[0][1]))

if __name__ == "__main__":
    print(isTradeDay('2018-09-03'))

