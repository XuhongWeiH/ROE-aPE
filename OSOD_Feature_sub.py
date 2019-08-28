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
            
            
           
            if len(yshizhi) < 3 or len(yROE) < 3:
                continue
            if max(shizhi.values()) < 1e8:
                continue
            # if max(guben.values())< 0*1e8:
            #     continue
            if yshizhi[-1] < yshizhi[-3]:
                continue
            if len(y) < 600:
                continue
            if np.mean(yROE[-3:]) < 12:
                continue
            if self.industry_dic[self.document['code']][1] in \
                    ['化工','计算机','国防军工','机械设备','建筑装饰','有色金属','商业贸易','采掘','钢铁'\
                    ,'电气设备','综合','汽车','电子']:
                continue

            print(code+','+self.industry_dic[self.document['code']][0]+','+self.industry_dic[self.document['code']][1]+','+str(np.max(yguben)/(1e10)))
            continue

        return 0
                

if __name__ == '__main__':
    stock = stockFeature('./data/stock_industry.csv')
    
    # stock.setupDateStore()
    # stock.updateStore(datetime.now().strftime("%Y-%m-%d"))
    stock_list = stock.peAnalyse()

