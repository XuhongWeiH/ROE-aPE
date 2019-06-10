from OSOD import oneStockDocument
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

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

            plt.figure(1)
            plt.subplot(211)
            plt.title('PE'+self.document['code'])
            plt.plot(x, y)
            plt.plot(x, [np.mean(y[1000:]) for i in range(len(y))])
            plt.plot(x, [np.max(y[1000:]) for i in range(len(y))])
            plt.plot(x, [np.min(y[1000:]) for i in range(len(y))])

            G = self.document['G']
            xg = [i for i in range(len(G.keys()))]
            yg = []
            for item in G.values():
                yg += [float(item)*100]
            yg = np.array(yg)
            plt.subplot(212)
            plt.plot(xg, yg)
            plt.title('G')
            plt.plot(xg, [np.mean(yg[-4:]) for i in range(len(yg))])
            plt.plot(xg, [np.max(yg[17:]) for i in range(len(yg))])
            plt.plot(xg, [np.min(yg[17:]) for i in range(len(yg))])

            
            plt.show()

if __name__ == '__main__':
    stock = stockFeature('./data/stock_industry_select.csv')
    # stock.setupDateStore()
    # stock.updateStore(datetime.now().strftime("%Y-%m-%d"))
    stock.peAnalyse()
        
