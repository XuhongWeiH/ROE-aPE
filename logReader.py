import json
import matplotlib.pyplot as plt
from pylab import * 
def viewableLog(log_file = './data2/out.json'):
    with open(log_file, 'r') as f:
        trade_list = json.load(fp=f)

    xianjing = 10
    shizhi = 0
    chicang_dic = {}
    jiagebodong = {}
    zhibiaobodong = {}
    riqibodong = {}

    for item in trade_list:
        if item[3] == "buy":
            chicang_dic[item[0]] = 1/item[2]
            jiagebodong[item[0]] = [item[2]]
            zhibiaobodong[item[0]] = [item[4]]
            riqibodong[item[0]] = [item[1]]
        elif item[3] == "hold":
            jiagebodong[item[0]] += [item[2]]
            zhibiaobodong[item[0]] += [item[4]]
            riqibodong[item[0]] += [item[1]]
        elif item[3] == "sold":
            xianjing += (chicang_dic[item[0]] * item[2] - 1)
            chicang_dic.pop(item[0])

                                #支持中文
    mpl.rcParams['font.sans-serif'] = ['SimHei']

   
    for k in zhibiaobodong.keys():  
        names = riqibodong[k]
        x = range(len(names))
        y = jiagebodong[k]
        y1= zhibiaobodong[k]
        #plt.plot(x, y, 'ro-')
        #plt.plot(x, y1, 'bo-')
        #pl.xlim(-1, 11)  # 限定横轴的范围
        #pl.ylim(-1, 110)  # 限定纵轴的范围
        plt.plot(x, y, marker='o', mec='r', mfc='w',label=u'价格')
        plt.plot(x, y1, marker='*', ms=10,label=u'指标')
        plt.legend()  # 让图例生效
        plt.xticks(x, names, rotation=45)
        plt.margins(0)
        plt.subplots_adjust(bottom=0.15)
        plt.xlabel(u"time(s)") #X轴标签
        plt.ylabel("RMSE") #Y轴标签
        plt.title("A simple plot") #标题

        plt.show()

    return xianjing

if __name__ == "__main__":
    print("盈利:", viewableLog())