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

def askPrice_byDate(code, sltDateBegin, sltDateEnd):

    lg = bs.login()

    rs = bs.query_history_k_data_plus(code,
        "date, code, open, high, low, close",
        start_date=sltDateBegin, end_date=sltDateEnd,
        frequency="d", adjustflag="2")

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    result = pd.DataFrame(data_list, columns=rs.fields)

    return result

if __name__ == "__main__":
    askPrice_byDate('sz.000651', '2016-01-01', '2016-10-02')