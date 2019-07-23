#-*- coding: utf-8 -*-
from OSOD import oneStockDocument
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
from baoK_line import askPrice_byDate
import matplotlib
from datetime import datetime, timedelta
import numpy as np
from bao_hongli import searchHongli

plt.style.use('ggplot') 
# font = {'family':'SimHei'} 
# matplotlib.rc('font',**font) 
# matplotlib.rcParams['axes.unicode_minus']=False

class stockFeature(oneStockDocument):
    
    def __init__(self, industry_root):
        oneStockDocument.__init__(self, industry_root)
        
    def peAnalyse(self):
        industry_dic = self.hangye_list()
        K_Dapan = {}
        xiangguandu = []
        df_dapan_Kline = askPrice_byDate(
            code='sh.000001', sltDateBegin='2008-01-01', sltDateEnd=datetime.now().strftime("%Y-%m-%d"))
        df = df_dapan_Kline[["date", "code", "open", "high", "low", "close","volume","amount"]]
        yk_dapan = []
        for item in df.values:
            date = item[0]
            K_Dapan[date] = (float(item[3]) + float(item[4]))/2
        for item in K_Dapan.values():
                yk_dapan += [float(item)]
        
        stock_list = []
        for code in industry_dic.keys():

            with open('./data_osod/' + code + '.json', 'r') as f:
                self.document = json.load(fp=f)

            if self.industry_dic[self.document['code']][1] in ['银行', '非银金融']:
                pb = self.document['PB']
                x = [i for i in range(len(pb.keys()))]
                y = []
                for item in pb.values():
                    y += [float(item)]
                y = np.array(y)
            else:
                pe = self.document['PE']
                x = [i for i in range(len(pe.keys()))]
                y = []
                for item in pe.values():
                    y += [float(item)]
                y = np.array(y)

            pcf = self.document['PCF']
            xpcf = [i for i in range(len(pcf.keys()))]
            ypcf = []
            for item in pcf.values():
                ypcf += [float(item)]
            ypcf = np.array(ypcf)

            pcf = self.document['PCF']

            kline = self.document['K_line']
            volume = self.document['volume']
            amount = self.document['amount']
            xk = [i for i in range(len(kline.keys()))]
            yk = []
            yk_vol = []
            yk_amt = []
            for item in kline.values():
                yk += [float(item)]
            for item in volume.values():
                yk_vol += [float(item)]
            for item in amount.values():
                yk_amt += [float(item)]
            yk = np.array(yk)
            yk_vol = np.array(yk_vol)
            yk_amt = np.array(yk_amt)

            G = self.document['G']
            xg = []
            yg = []
            count = 0
            for item in G.keys():
                # if item.split('-')[1] == '4':
                xg += [count]
                yg += [float(G[item])*100]
                count += 1
            yg = np.array(yg)

            ProG = self.document['ProG']
            xProG = []
            yProG = []
            count = 0
            for item in ProG.keys():
                # if item.split('-')[1] == '4':
                    xProG += [count]
                    yProG += [float(ProG[item])*100]
                    count += 1
            yProG = np.array(yProG)

            ROE = self.document['ROE']
            xROE = []
            yROE = []
            count = 0
            for item in ROE.keys():
                if item.split('-')[1] == '4':
                    xROE += [count]
                    yROE += [float(ROE[item])*100]
                    count += 1
            yROE = np.array(yROE)

            shizhi = self.document['shizhi']
            xshizhi = []
            yshizhi = []
            count = 0
            for item in shizhi.keys():
                if item.split('-')[1] == '4':
                    xshizhi += [count]
                    yshizhi += [float(shizhi[item])*100]
                    count += 1
            yshizhi = np.array(yshizhi)

            guben = self.document['guben']
            xguben = []
            yguben = []
            count = 0
            for item in guben.keys():
                xguben += [count]
                yguben+= [float(guben[item])*100]
                count += 1
            yguben = np.array(yguben)
            
            peg = y[-1] / ((yshizhi[-1]/yshizhi[-3])**0.5 - 1)/100
           
            # if len(yshizhi) < 3 or len(yROE) < 3:
            #     continue
            # if max(shizhi.values()) < 1e8:
            #     continue
            # if yshizhi[-1] < yshizhi[-3]:
            #     continue
            # if len(y) < 600:
            #     continue
            # if np.mean(yROE[-5:]) < 12:
            #     continue

            if len(y)<600:
                pe_max =  np.max(y[-400:])
                pe_mean = np.mean(y[-400:])
                pe_min =  np.min(y[-400:])
            else:
                pe_max =  np.max(y[-600:])
                pe_mean = np.mean(y[-600:])
                pe_min =  np.min(y[-600:])
            price_max = np.max(yk[-120:])
            price_min = np.min(yk[-120:])
            if self.industry_dic[self.document['code']][1] in ['银行']:
                jiagetidu = np.array([1+0.01*i for i in range(-2,3,1)])
            else:
                jiagetidu = np.array([1+0.035*i for i in range(-2,3,1)])

            #过年要改年份
            fenhong = searchHongli(self.document['code'], 2019)
            if fenhong.empty:
                fenhong = searchHongli(self.document['code'], 2018)
                if fenhong.empty:
                    # print('抠门公司无分红->')
                    continue
            #     else:
            #         print('年份:2018',fenhong.values[0])
            #         print('股息率%.2f%%,%s'%(100*float(fenhong.values[0][-2])/yk[-1], fenhong.values[0][3]),'当前股价:',yk[-1])
            # else:
            #     print('年份:2019',fenhong.values[0])
            #     print('股息率%.f%%,%s'%(100*float(fenhong.values[0][-2])/yk[-1], fenhong.values[0][3]),'当前股价:',yk[-1])

            
            kaocha_day = min(900,len(yk))
            yk_dapan_sub = yk_dapan[-kaocha_day:]
            yk_sub = yk[-kaocha_day:]
            ab = np.array([yk_dapan_sub, yk_sub])
            cor = np.corrcoef(ab)
            xiangguandu += [cor[1][0]]
            additional = ''
            if cor[1][0] > 0.1 :
                if (np.mean(yROE[-5:]) < 15 or (y[-1]-pe_min)/(pe_max-pe_min)*100//1 > 15):
                    pass
                    continue
                else:
                    additional = '-防御性不高，行情不好不要买'
                    # continue#
                    
                    # if 100*(yk[-1]/((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1])-1) > 10:
                    #     continue
                    
            else:
                pass
                # if 100*(yk[-1]/((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1])-1) > 15:
                #     continue
                # continue
                
            if y[-1] > 45:
                additional += "pe过45，不建议买入"
                # continue
            

            #test
            # print(code+','+self.industry_dic[self.document['code']][0]+','+self.industry_dic[self.document['code']][1]+','+'申万一级行业')

            shuchuxiane = 101
            if False or (y[-1]-pe_min)/(pe_max-pe_min)*100 < shuchuxiane:
                
                outstr = ' '.join([self.industry_dic[self.document['code']][0],\
                    self.industry_dic[self.document['code']][1],\
                    str(max(shizhi.values())//1e8),'亿利润, 价估:%.2f %%'%((y[-1]-pe_min)/(pe_max-pe_min)*100),\
                    "\n当前价格<%s:%.2f元>,"%(max(kline.keys()),yk[-1]),\
                    "\n买入估值参考:",str(pe_min*yk[-1]/y[-1]*jiagetidu*100//1/100),\
                    "\n买入价格参考:",str(price_min*jiagetidu*100//1/100),\
                    "\n买入平均参考:",str((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu*100//1/100),\
                    "\n卖出估值保守:",str(pe_mean*yk[-1]/y[-1]*jiagetidu*100//1/100),\
                    "\n卖出价格保守:",str(price_max*jiagetidu*100//1/100),\
                    "\n卖出估值激进:",str(pe_max*yk[-1]/y[-1]*jiagetidu*100//1/100),\
                    "\n五年平均杜邦ROE %.2f%%"%(np.mean(yROE[-5:])),\
                    "\n当前PETTM=%.2f,(银行金融为PBTTM), peg:%.2f"%(y[-1],peg), \
                    '\n股息率%.2f%%,上次分红日期:%s'%(100*float(fenhong.values[0][-2])/yk[-1], fenhong.values[0][3]),\
                    "\n平均建仓参考: %.2f￥, 当前涨幅%.2f%%"%((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1], 100*(yk[-1]/((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1])-1)),\
                    "\n防御力(越大越好,优质股基准为90%%):%.2f%% %s"%((1 - cor[1][0])*100, additional),\
                    '\n'])
                stock_list += [((y[-1]-pe_min)/(pe_max-pe_min)*100,100*(yk[-1]/((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1])-1),outstr)]
                # print(outstr)
            else:
                continue

            if False:
                print(outstr)
                plt.figure(1,figsize=(13,7))
                plt.subplot(321)
                plt.title('PE沪'+self.document['code'] + '_' + str(max(shizhi.values())/1e8))
                plt.ylim(np.min(yk)-5, np.max(yk)+5)
                # plt.plot(x, y)
                try:
                    plt.plot(xk, yk,'r')
                except ValueError:
                    print('yk is not len x =')
                    continue
                    pass

                # plt.plot(x, [np.mean(y[-800:]) for i in range(len(y))])
                # plt.plot(x, [np.max(y[-800:]) for i in range(len(y))])
                # plt.plot(x, [np.min(y[-800:]) for i in range(len(y))])
                
                plt.subplot(322)
                plt.ylim(pe_min-1,pe_max+1)
                plt.plot(x, y)
                plt.title('PEorPB_' + 'PEG=' + str(y[-1] / ((yshizhi[-1]/yshizhi[-3])**0.5 - 1)/100)[:5])
                plt.plot(x, [pe_mean for i in range(len(y))])
                plt.plot(x, [pe_max for i in range(len(y))])
                plt.plot(x, [pe_min for i in range(len(y))])

                # plt.subplot(323)
                # plt.ylim(np.min(ypcf[-600:]),np.max(ypcf[-600:]))
                # plt.plot(xpcf, ypcf)
                # plt.title('PCF')
                # plt.plot(xpcf, [np.mean(ypcf[-600:]) for i in range(len(ypcf))])
                # plt.plot(xpcf, [np.max(ypcf[-600:]) for i in range(len(ypcf))])
                # plt.plot(xpcf, [np.min(ypcf[-600:]) for i in range(len(ypcf))])

                # plt.subplot(323)
                # plt.plot(xProG, yProG)
                # plt.title('net profits growth rate')
                # plt.plot(xProG, [np.max(yProG) for i in range(len(yProG))])
                # plt.plot(xProG, [np.min(yProG) for i in range(len(yProG))])

                plt.subplot(324)
                plt.plot(xROE, yROE)
                plt.title('ROE')
                plt.plot(xROE, [15 for i in range(len(yROE))],'b--')
                # plt.plot(xROE, [12 for i in range(len(yROE))],'r--')
                plt.plot(xROE, [np.mean(yROE[-5:]) for i in range(len(yROE))],'g')

                plt.subplot(326)
                plt.plot(xshizhi, yshizhi)
                plt.title('Net Profits Value')
                plt.plot(xshizhi, [min(yshizhi) for i in range(len(yshizhi))])

                # plt.subplot(326)
                # plt.plot(xguben, yguben)
                # plt.title('Circulation market value ')
                # plt.plot(xguben, [min(yguben) for i in range(len(yguben))])
                # plt.show()

                
                #相关度考察
                plt.subplot(323)
                plt.title('dapan%.2f--mean:%.2f'%(cor[1][0], np.mean(xiangguandu)))
                plt.plot([i for i in range(kaocha_day)], yk_dapan_sub,'g')
            
                plt.subplot(325)
                plt.plot([i for i in range(kaocha_day)], yk_sub,'r')
                # plt.plot(xk, yk_vol,'g')
                plt.title('yk'+ str(kaocha_day))

                plt.show()
        return stock_list
                

if __name__ == '__main__':
    stock = stockFeature('./data/stock_industry_select630.csv')
    # stock = stockFeature('./data/stock_industry_select_chicang.csv')
    
    stock.setupDateStore()
    stock.updateStore(datetime.now().strftime("%Y-%m-%d"))
    stock_list = stock.peAnalyse()
    stock_list = sorted(stock_list, key=lambda s: s[1])
    print('================')
    i = 1
    for item in stock_list:
        print(str(i) + ' ' + item[2])
        i += 1
