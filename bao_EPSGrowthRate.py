import baostock as bs
import pandas as pd
import time
def computeG(code, year, quarter):
 # 查询杜邦指数
    growth_list = []
    rs_growth = bs.query_growth_data(code=code, year=year, quarter=quarter)
    while (rs_growth.error_code == '0') & rs_growth.next():
        growth_list.append(rs_growth.get_row_data())
    result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
    # 打印输出
    return result_growth

def compute_total_G(yearSE):
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    # print('login respond error_code:' + lg.error_code)
    # print('login respond error_msg:' + lg.error_msg)
    # 获取全部证券基本资料
    rs = bs.query_stock_basic ()
    # rs = bs.query_stock_basic(code_name="浦发银行") # 支持模糊查询
    # print('query_stock_basic respond error_code:' + rs.error_code)
    # print('query_stock_basic respond error_msg:' + rs.error_msg)
    result_profit = pd.DataFrame()

    jingduCount = 0
    startt = time.time()
    
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        code = rs.get_row_data()[0]
        jingduCount += 1
        newt = time.time()
        lg = bs.login()
        print('\r',"进度:%.2f%% | Code:%s | End@:%s | year:%d~%d"                                                                % (100*jingduCount/len(rs.data), code, 
        time.asctime( time.localtime(newt+(newt - startt)/jingduCount*(len(rs.data) - jingduCount))),
          yearSE[0], yearSE[1]),end='   ')

        for year in range(yearSE[0], yearSE[1]):
            
            for season in range(1,5):
                df = computeG(code, year, season)
                if df.empty:
                    continue
                else:
                    df['season']=season
                    df['year']=year
                    if result_profit.empty:
                        result_profit = df
                    else:
                        result_profit = result_profit.append(df)
    # 原始数据存储
    result_profit.to_csv("./data/G_"+str(yearSE)+".csv",encoding="utf-8", index=False)
    # 筛选有用数据
    # result = result_profit[['code', 'dupontROE']]
    # result = result[result['dupontROE'] != '']
    # result['dupontROE'] = result['dupontROE'].astype(float)
    # series_mean = result.groupby(by=['code'])['dupontROE'].mean()
    # series_std = result.groupby(by=['code'])['dupontROE'].std()
    # df2 = pd.DataFrame({'mean': series_mean.data, 'std':series_std.data},\
    #         columns=['mean', 'std'], index=series_mean.index)
    # df2 = df2.sort_values(['mean'])
    # df2.to_csv("./data3/dupont_data_sorted_by_roe.csv", encoding="gbk",index=True)
    # 登出系统
    bs.logout()

if __name__ == '__main__':
     compute_total_G(yearSE = [2006, 2020])