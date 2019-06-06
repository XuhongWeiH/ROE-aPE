import pandas as pd
from bao_PE import get_bao_PE_byCode
from bao_tradeDay import isTradeDay
from datetime import datetime, timedelta
from baoK_line import askPrice_byDate
import json
from tqdm import tqdm
import os


class oneStockDocument:

    def __init__(self):

        self.industry_dic = self.hangye_list()
        self.code = ""
        self.name = ""
        self.industury = ""

        self.ROE = {}
        self.PE = {}
        self.G = {}
        self.K_line = {}

        self.document = {"code": self.code,
                         "name": self.name,
                         "industury": self.industury,
                         "ROE": self.ROE,
                         "PE": self.PE,
                         "G": self.G,
                         "K_line": self.K_line
                         }

        self.df_origin_ROE = pd.read_csv('./data/ROE_[2006, 2020].csv')
        self.df_origin_G = pd.read_csv('./data/G_[2006, 2020].csv')

    def hangye_list(self):
        df_industry = pd.read_csv('./data/stock_industry.csv')
        df_industry = df_industry[['code', 'code_name', 'industry']]
        industry_dic = {}
        for item in df_industry.values:
            industry_dic[item[0]] = item[1:3]
        return industry_dic

    def setDocument(self):
        self.document = {"code": self.code,
                         "name": self.name,
                         "industury": self.industury,
                         "ROE": self.ROE,
                         "PE": self.PE,
                         "G": self.G,
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
        self.K_line = {}

    def readROE(self):

        df = self.df_origin_ROE[['code', 'dupontROE', 'season', 'year']][(
            self.df_origin_ROE["code"] == self.code)]

        for item in df.values:
            year = item[3]
            season = item[2]
            self.ROE['-'.join([str(year), str(season)])] = item[1]

    def readG(self):

        df = self.df_origin_G[['code', 'YOYEPSBasic', 'season', 'year']][(
            self.df_origin_G["code"] == self.code)]

        for item in df.values:
            year = item[3]
            season = item[2]
            if item[1] < 100:
                self.G['-'.join([str(year), str(season)])] = item[1]

    def readPE(self):
        df_origin_PE = get_bao_PE_byCode(
            code=self.code, sltDateBegin='2008-01-01', sltDateEnd='2019-04-30')
        df = df_origin_PE[['date', 'code', 'peTTM']]

        for item in df.values:
            date = item[0]
            self.PE[date] = item[2]

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
            if os.path.exists(code + '.json'):
                continue
            self.code = code
            self.industry = self.industry_dic[code][1]
            self.name = self.industry_dic[code][0]
            self.readROE()
            self.readG()
            self.readPE()
            self.readK_line()
            self.setDocument()


if __name__ == '__main__':
    store = oneStockDocument()
    store.setupDateStore()
