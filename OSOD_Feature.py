#-*- coding: utf-8 -*-
from OSOD import oneStockDocument
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
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
        for code in industry_dic.keys():
            
            with open('./data_osod/' + code + '.json', 'r') as f:
                self.document = json.load(fp=f)

            pe = self.document['PE']
            x = [i for i in range(len(pe.keys()))]
            y = []
            for item in pe.values():
                y += [float(item)]
            y = np.array(y)

            kline = self.document['K_line']
            yk = []
            for item in kline.values():
                yk += [float(item)]
            yk = np.array(yk)

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
            
            #if
            if y[-1] > 30:
                continue

            if max(shizhi.values()) < 1e9:
                continue

            if yshizhi[-1]/yshizhi[-3] < 0:
                continue

            peg = y[-1] / ((yshizhi[-1]/yshizhi[-3])**0.5 - 1)/100
            if peg > 10 or y[-1] / peg < 0.05:
                continue

            # if y[-1] > (np.mean(y[1000:]) - np.min(y[1000:]))/2*2 + np.min(y[1000:]):
            #     continue

            if np.mean(yROE[-3:]) < 12:
                continue
            if self.industry_dic[self.document['code']][1] in ['化工','采掘','机械设备','钢铁','传媒','有色金属']:
                continue
            if yshizhi[-1] < yshizhi[-2]:
                continue

            print(self.industry_dic[self.document['code']] , peg, max(shizhi.values())/1e8)
            fenhong = searchHongli(self.document['code'], 2019)
            if fenhong.empty:
                fenhong = searchHongli(self.document['code'], 2018)
                if fenhong.empty:
                    print('抠门公司无分红')
                else:
                    print('年份:2018',fenhong.values[0])
                    print('股息率%.2f%%'%(100*float(fenhong.values[0][-2])/yk[-1]),'当前股价:',yk[-1])
            else:
                print('年份:2019',fenhong.values[0])
                print('股息率%.2f%%'%(100*float(fenhong.values[0][-2])/yk[-1]),'当前股价:',yk[-1])
            
            if False:
                if len(yk) != len(x):
                    continue
                plt.clf()
                plt.figure(1,figsize=(13,7))
                plt.subplot(321)
                plt.title('PE沪'+self.document['code'] + '_' + str(max(shizhi.values())/1e8))
                plt.ylim(min(np.min(y[-1400:]),min(yk))-3, max(min(np.max(y[-1400:]),60), max(yk))+3)
                plt.plot(x, y)
                try:
                    plt.plot(x, yk,'r--')
                except ValueError:
                    plt.show()
                    continue
                    pass
                plt.plot(x, [np.mean(y[-800:]) for i in range(len(y))])
                plt.plot(x, [np.max(y[-800:]) for i in range(len(y))])
                plt.plot(x, [np.min(y[-800:]) for i in range(len(y))])
                
                plt.subplot(322)
                plt.ylim(-50,max(50,yg[-1])+10)
                plt.plot(xg, yg)
                plt.title('G_' + 'PEG=' + str(y[-1] / ((yshizhi[-1]/yshizhi[-3])**0.5 - 1)/100))
                plt.plot(xg, [np.mean(yg[-4:]) for i in range(len(yg))])
                plt.plot(xg, [np.max(yg[17:]) for i in range(len(yg))])
                plt.plot(xg, [np.min(yg[17:]) for i in range(len(yg))])

                plt.subplot(323)
                plt.plot(xProG, yProG)
                plt.title('ProG')
                plt.plot(xProG, [np.max(yProG) for i in range(len(yProG))])
                plt.plot(xProG, [np.min(yProG) for i in range(len(yProG))])

                plt.subplot(324)
                plt.plot(xROE, yROE)
                plt.title('ROE')
                plt.plot(xROE, [15 for i in range(len(yROE))])
                plt.plot(xROE, [np.mean(yROE[-3:]) for i in range(len(yROE))])

                plt.subplot(325)
                plt.plot(xshizhi, yshizhi)
                plt.title('shizhi')
                plt.plot(xshizhi, [min(yshizhi) for i in range(len(yshizhi))])
                plt.show()

if __name__ == '__main__':
    stock = stockFeature('./data/stock_industry.csv')
    # stock.setupDateStore()
    # stock.updateStore(datetime.now().strftime("%Y-%m-%d"))
    stock.peAnalyse()
        
