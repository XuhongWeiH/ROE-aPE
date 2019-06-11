import pandas as pd
from bao_PE import get_bao_PE_byCode
from bao_tradeDay import isTradeDay
from datetime import datetime, timedelta
from baoK_line import askPrice_byDate
import json
from tqdm import tqdm
from bao_ROE import computeROE
from bao_EPSGrowthRate import computeG
import os
from bao_profit import computeProfit


class oneStockDocument():

    def __init__(self, industry_root):

        self.code = ""
        self.name = ""
        self.industry = ""
        self.industry_root = industry_root
        self.industry_dic = self.hangye_list()

        self.ROE = {}
        self.PE = {}
        self.G = {}
        self.ProG = {}
        self.K_line = {}
        self.shizhi = {}

        self.document = {"code": self.code,
                         "name": self.name,
                         "industry": self.industry,
                         "ROE": self.ROE,
                         "PE": self.PE,
                         "G": self.G,
                         "ProG":self.ProG,
                         "shizhi": self.shizhi,
                         "K_line": self.K_line
                         }

        self.df_origin_ROE = pd.read_csv('./data/ROE_[2006, 2020].csv')
        self.df_origin_G = pd.read_csv('./data/G_[2006, 2020].csv')
        self.df_origin_Profit = pd.read_csv('./data/Profit_[2015, 2020].csv')

    def hangye_list(self):
        df_industry = pd.read_csv(self.industry_root)
        df_industry = df_industry[['code', 'code_name', 'industry']]
        industry_dic = {}
        for item in df_industry.values:
            industry_dic[item[0]] = item[1:3]
        return industry_dic

    def setDocument(self):
        self.document = {"code": self.code,
                         "name": self.name,
                         "industry": self.industry,
                         "ROE": self.ROE,
                         "PE": self.PE,
                         "G": self.G,
                         "ProG": self.ProG,
                         "shizhi": self.shizhi,
                         "K_line": self.K_line
                         }
        with open('./data_osod/' + self.code + '.json', 'w') as f:
            json.dump(self.document, f)

    def clearDateVolum(self):
        self.code = ""
        self.name = ""
        self.industury = ""

        self.ROE = {}
        self.PE = {}
        self.G = {}
        self.ProG = {}
        self.K_line = {}
        self.shizhi = {}

    def readROE(self):

        df = self.df_origin_ROE[['code', 'dupontROE', 'season', 'year']][(
            self.df_origin_ROE["code"] == self.code)]

        for item in df.values:
            year = item[3]
            season = item[2]
            self.ROE['-'.join([str(year), str(season)])] = item[1]

    def readG(self):

        df = self.df_origin_G[['code', 'YOYEPSBasic', 'YOYNI', 'season', 'year']][(
            self.df_origin_G["code"] == self.code)]

        for item in df.values:
            year = item[4]
            season = item[3]
            if item[1] < 1000 and item[2] < 1000:
                self.G['-'.join([str(year), str(season)])] = float(item[1])
                self.ProG['-'.join([str(year), str(season)])] = float(item[2])

    def readProfitTotal(self):

        df = self.df_origin_Profit[['code', 'netProfit', 'season', 'year']][(
            self.df_origin_Profit["code"] == self.code)]

        for item in df.values:
            year = item[3]
            season = item[2]
            if item[1] < 1e20 :
                self.shizhi['-'.join([str(year), str(season)])] = float(item[1])

    def readPE(self):
        df_origin_PE = get_bao_PE_byCode(
            code=self.code, sltDateBegin='2008-01-01', sltDateEnd='2019-04-30')
        df = df_origin_PE[['date', 'code', 'peTTM']]

        for item in df.values:
            date = item[0]
            self.PE[date] = float(item[2])

    def readK_line(self):
        df_origin_Kline = askPrice_byDate(
            code=self.code, sltDateBegin='2008-01-01', sltDateEnd='2019-04-30')
        df = df_origin_Kline[["date", "code", "open", "high", "low", "close"]]

        for item in df.values:
            date = item[0]
            self.K_line[date] = (float(item[3]) + float(item[4]))/2

    def setupDateStore(self):
        self.clearDateVolum()
        for code in tqdm(self.industry_dic.keys()):
            if os.path.exists('./data_osod/' + code + '.json'):
                continue
            self.code = code
            self.industry = self.industry_dic[code][1]
            self.name = self.industry_dic[code][0]
            self.readROE()
            self.readG()
            self.readProfitTotal()
            self.readPE()
            self.readK_line()
            self.setDocument()

    def updateStore(self, todayEnd):
        for code in tqdm(self.industry_dic.keys()):
            assert(os.path.exists('./data_osod/' + code + '.json'))

            with open('./data_osod/' + code + '.json', 'r') as f:
                self.document = json.load(fp=f)
            
            #ROE
            self.ROE = self.document['ROE']
            while True:
                ROE_latest = max(self.ROE.keys())
                year_latest = int(ROE_latest.split('-')[0])
                season_latest = int(ROE_latest.split('-')[1])
                ROE_newyear = year_latest
                ROE_newSea = season_latest + 1
                if ROE_newSea == 5:
                    ROE_newyear = year_latest + 1
                    ROE_newSea = 1
                df = computeROE(code, ROE_newyear, ROE_newSea)
                if df.empty:
                    break
                df['season']=ROE_newSea
                df['year']=ROE_newyear
                df = df[['code', 'dupontROE', 'season', 'year']]
                if df.values[0][1] != '':
                    self.ROE['-'.join([str(ROE_newyear), str(ROE_newSea)])] = float(df.values[0][1])
                else:
                    self.ROE['-'.join([str(ROE_newyear), str(ROE_newSea)])] = 0
            #G and ProG
            self.G = self.document['G']
            self.ProG = self.document['ProG']
            while True:
                G_latest = max(self.G.keys())
                year_latest = int(G_latest.split('-')[0])
                season_latest = int(G_latest.split('-')[1])
                G_newyear = year_latest
                G_newSea = season_latest + 1
                if G_newSea == 5:
                    G_newyear = year_latest + 1
                    G_newSea = 1
                df = computeG(code, G_newyear, G_newSea)
                if df.empty:
                    break
                df['season']=G_newSea
                df['year']=G_newyear
                df = df[['code', 'YOYEPSBasic','YOYNI', 'season', 'year']]
                self.G['-'.join([str(G_newyear), str(G_newSea)])] = float(df.values[0][1])
                self.ProG['-'.join([str(ProG_newyear), str(ProG_newSea)])] = float(df.values[0][2])
            # shizhi
            self.shizhi = self.document['shizhi']
            while True:
                shizhi_latest = max(self.shizhi.keys())
                year_latest = int(shizhi_latest.split('-')[0])
                season_latest = int(shizhi_latest.split('-')[1])
                shizhi_newyear = year_latest
                shizhi_newSea = season_latest + 1
                if shizhi_newSea == 5:
                    shizhi_newyear = year_latest + 1
                    shizhi_newSea = 1
                df = computeProfit(code, shizhi_newyear, shizhi_newSea)
                if df.empty:
                    break
                df['season']=shizhi_newSea
                df['year']=shizhi_newyear
                df = df[['code', 'netProfit', 'season', 'year']]
                self.shizhi['-'.join([str(G_newyear), str(G_newSea)])] = float(df.values[0][1])
            
            #PE
            self.PE = self.document['PE']
            df = get_bao_PE_byCode(code=code,\
                                   sltDateBegin=max(self.PE.keys()), \
                                   sltDateEnd=todayEnd)
            df = df[['date', 'code', 'peTTM']]

            for item in df.values:
                date = item[0]
                self.PE[date] = item[2]

            #K_line
            self.K_line = self.document['K_line']
            df = askPrice_byDate(code=code, \
                                            sltDateBegin=max(self.K_line.keys()), \
                                            sltDateEnd=todayEnd)
            df = df[["date", "code", "open", "high", "low", "close"]]
            
            for item in df.values:
                date = item[0]
                self.K_line[date] = (float(item[3]) + float(item[4]))/2

            self.document["ROE"] = self.ROE
            self.document["PE"] = self.PE
            self.document["G"] = self.G
            self.document["ProG"] = self.ProG
            self.document["K_line"] = self.K_line
            with open('./data_osod/' + code + '.json', 'w') as f:
                json.dump(self.document, f)
                         

            

if __name__ == '__main__':
    store = oneStockDocument(industry_root = './data/stock_industry.csv')
    # store.setupDateStore()
    store.updateStore(datetime.now().strftime("%Y-%m-%d"))