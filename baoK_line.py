import baostock as bs
import pandas as pd

def askPrice(code, date):

    lg = bs.login()

    rs = bs.query_history_k_data_plus(code,
        "date, code, open, high, low, close",
        start_date=date, end_date=date,
        frequency="d", adjustflag="2")

    #### 打印结果集 ####
    data_list = []
    if (rs.error_code == '0') & rs.next():
        return rs.get_row_data()
    else:
        raise ValueError

if __name__ == "__main__":
    try:
        print(askPrice("sh.600230", "2019-04-06"))
    except ValueError:
        print('catched')