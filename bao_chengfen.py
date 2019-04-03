import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取行业分类数据
rs = bs.query_stock_industry()
# rs = bs.query_stock_basic(code_name="浦发银行")
print('query_stock_industry error_code:'+rs.error_code)
print('query_stock_industry respond  error_msg:'+rs.error_msg)

# 打印结果集
industry_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    rs_code = rs.get_row_data()
    if rs_code[3] != '':
        industry_list.append(rs_code[1:])
result = pd.DataFrame(industry_list, columns=rs.fields[1:])
# 结果集输出到csv文件
result.to_csv("./data/stock_industry.csv", encoding="utf-8", index=False)
print(result)

# 登出系统
bs.logout()