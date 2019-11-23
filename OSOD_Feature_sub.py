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
        
    def peAnalyse(self, testyear):
        industry_dic = self.hangye_list()
        
        for code in industry_dic.keys():

            with open('./data_osod/' + code + '.json', 'r') as f:
                self.document = json.load(fp=f)
            # if self.industry_dic[self.document['code']][0] in ['洽洽食品']:
            #     print(1)
            # else:
            #     continue
            if self.industry_dic[self.document['code']][1] in ['银行', '非银金融']:
                pb = self.document['PB']
                y = []
                for item in pb.keys():
                    if item < testyear:
                        y += [float(pb[item])]
                y = np.array(y)
            else:
                pe = self.document['PE']
                y = []
                for item in pe.keys():
                    if item < testyear:
                        y += [float(pe[item])]
                y = np.array(y)

            ROE = self.document['ROE']
            yROE = []
            for item in ROE.keys():
                if item.split('-')[1] == '4':
                    if item.split('-')[0] < testyear.split('-')[0]:
                        yROE += [float(ROE[item])*100]
            yROE = np.array(yROE)

            shizhi = self.document['shizhi']
            yshizhi = []
            for item in shizhi.keys():
                if item.split('-')[1] == '4':
                    if item.split('-')[0] < testyear.split('-')[0]:
                        yshizhi += [float(shizhi[item])*100]
            yshizhi = np.array(yshizhi)

            guben = self.document['guben']
            yguben = []
            for item in guben.keys():
                if item < testyear:
                    if item.split('-')[0] < testyear.split('-')[0]:
                        yguben+= [float(guben[item])*100]
            yguben = np.array(yguben)
            
            if len(yshizhi) < 3 or len(yROE) < 3:
                continue
            if len(y) < 600:
                continue
            if shizhi == {} or max(shizhi.values()) < 5e7:
                continue
            # if max(guben.values())< 0*1e8:
            #     continue
            # if yshizhi[-1] < yshizhi[-3]:
            #     continue
            
            if np.mean(yROE[-4:]) < 14:
                continue
            if self.industry_dic[self.document['code']][1] in \
                    ['化工','计算机','国防军工','机械设备','建筑装饰','有色金属','商业贸易','采掘','钢铁'\
                    ,'电气设备','综合','汽车','电子','建筑材料','轻工制造','纺织服装','交通运输','公用事业','传媒','通信']:
                continue

            print(code+','+self.industry_dic[self.document['code']][0]+','+self.industry_dic[self.document['code']][1]+','+'申万一级行业')
            continue

        return 0
                

if __name__ == '__main__':
    stock = stockFeature('./data/stock_industry.csv')
    
    # stock.setupDateStore()
    # stock.updateStore(datetime.now().strftime("%Y-%m-%d"))
    # stock.updateStore(datetime.now().strftime("2011-03-06"))
    stock_list = stock.peAnalyse('2019-05-10')

