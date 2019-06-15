import baostock as bs
import pandas as pd

def searchHongli(code, year):
    lg = bs.login()

    rs_list = []
    rs_dividend = bs.query_dividend_data(code=code, year = year,yearType="report")
    #@param yearType: 年份类别，默认为"report":预案公告年份，可选项"operate":除权除息年份
    while (rs_dividend.error_code == '0') & rs_dividend.next():
        rs_list.append(rs_dividend.get_row_data())

    result_dividend = pd.DataFrame(rs_list, columns=rs_dividend.fields)
    result = result_dividend[['code',\
        'dividPlanAnnounceDate','dividPlanDate','dividRegistDate','dividOperateDate',\
        'dividCashPsBeforeTax','dividCashStock']]
    return result

if __name__ == '__main__':
    hongli= searchHongli('sh.600585',2018)
    print(hongli.values)
