#coding:utf-8
import json
import matplotlib.pyplot as plt
from pylab import * 
import pandas as pd

def hangyeRead():
    df_industry=pd.read_csv('./data/stock_industry.csv')
    df_industry = df_industry[['code','code_name','industry']]
    industry_dic = {}
    for item in df_industry.values:
        industry_dic[item[0]] = item[1:3]

    return industry_dic

def viewableLog(log_file = './data2/out.json'):
    with open(log_file, 'r') as f:
        trade_list = json.load(fp=f)

    xianjing = 10
    shizhi = 0
    chicang_dic = {}
    jiagebodong = {}
    zhibiaobodong = {}
    riqibodong = {}
    industry_dic = hangyeRead()

    for item in trade_list:
        if item[3] == "buy":
            chicang_dic[item[0]] = 1/item[2]
            try:
                jiagebodong[item[0]] += [item[2]]
                zhibiaobodong[item[0]] += [item[4]]
                riqibodong[item[0]] += [item[1]]
            except KeyError:  
                jiagebodong[item[0]] = [item[2]]
                zhibiaobodong[item[0]] = [item[4]]
                riqibodong[item[0]] = [item[1]]
        elif item[3] == "hold":
            jiagebodong[item[0]] += [item[2]]
            zhibiaobodong[item[0]] += [item[4]]
            riqibodong[item[0]] += [item[1]]
        # elif item[3] == "sold":
        #     xianjing += (chicang_dic[item[0]] * item[2] - 1)
        #     chicang_dic.pop(item[0])
            

                                #支持中文
    mpl.rcParams['font.sans-serif'] = ['SimHei']

    jidu = [1.0, 1.0]
    limit = [-6,-3]
    for k in zhibiaobodong.keys(): 
        if zhibiaobodong[k][0] > 2.5:
            jidu[0] = 2.0
        else:
            jidu[0] = 1.0
        names = riqibodong[k]
        x = range(len(names))
        y = jiagebodong[k]
        y1= zhibiaobodong[k]
        # if k == 'sh.600309':
        #     zhibiaobodong[k][0]=0
        y_buy = [limit[0] for b in range(len(names))]
        y_sold = [zhibiaobodong[k][0]-3.0*jidu[0] for b in range(len(names))]
        
        y_so2 = [zhibiaobodong[k][0]- jidu[0] for b in range(len(names))]
        y_so3 = [zhibiaobodong[k][0]+ jidu[0] for b in range(len(names))]
        y_so4 = [zhibiaobodong[k][0]for b in range(len(names))]
        y_so3_5 = [zhibiaobodong[k][0]+2*jidu[0] for b in range(len(names))]
        y_so51 = [zhibiaobodong[k][0]+4*jidu[0] for b in range(len(names))]
        y_so52 = [zhibiaobodong[k][0]+6*jidu[0] for b in range(len(names))]
        y_so53 = [zhibiaobodong[k][0]+9*jidu[0] for b in range(len(names))]
        y_so54 = [zhibiaobodong[k][0]+11*jidu[0] for b in range(len(names))]
        #plt.plot(x, y, 'ro-')
        #plt.plot(x, y1, 'bo-')
        #pl.xlim(-1, 11)  # 限定横轴的范围
        plt.ylim(-20, 40)  # 限定纵轴的范围
        plt.scatter(x, y, marker='.',label=u'price')
        plt.scatter(x, y1, marker='.', label=u'zhibiao')
        plt.plot(x, y_buy, marker='_',label=u'buy')
        plt.plot(x, y_sold, marker='_', label=u'0/4')
        plt.plot(x, y_so2, marker='_', label=u'1/4')
        plt.plot(x, y_so3, marker='_', label=u'3/4')
        plt.plot(x, y_so4, marker='_', label=u'2/4')
        plt.plot(x, y_so3_5, marker='_', label=u'4/4')
        plt.plot(x, y_so51, marker='_', label=u'5/4')
        plt.plot(x, y_so52, marker='_', label=u'6/4')
        plt.plot(x, y_so53, marker='_', label=u'7/4')
        plt.plot(x, y_so54, marker='_', label=u'8/4')
        plt.legend()  # 让图例生效
        # plt.xticks(x, names, rotation=90)
        # plt.margins(0)
        plt.subplots_adjust(bottom=0.15)
        plt.xlabel(u"time(s)") #X轴标签
        plt.ylabel(k) #Y轴标签
        plt.title(k +' ' + riqibodong[k][0]) #标题

        plt.show()

    return xianjing


if __name__ == "__main__":
    viewableLog(log_file = './data2/out.json')