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
        
    def peAnalyse(self, dapan_day):
        industry_dic = self.hangye_list()
        K_Dapan = {}
        xiangguandu = []
        df_dapan_Kline = askPrice_byDate(
            code='sh.000001', sltDateBegin='2008-01-01', sltDateEnd=dapan_day)
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
            
            if len(yshizhi) < 5:
                pass
                
                y1g = (yshizhi[-1]/yshizhi[-2] - 1)
                growth0 = min(0.35, y1g)
                growth =0.8*growth0
                PEG = y[-1] / growth /100
                # continue
            else:
                y4g = (yshizhi[-4]/yshizhi[-5] - 1)
                y3g = (yshizhi[-3]/yshizhi[-4] - 1)
                y2g = (yshizhi[-2]/yshizhi[-3] - 1)
                y1g = (yshizhi[-1]/yshizhi[-2] - 1)
                growth0 = min(0.35, y4g)*0.22 +min(0.35, y3g)*0.24 + min(0.35, y2g)*0.26 + min(0.35, y1g)*0.28
                growth =growth0
                PEG = y[-1] / growth /100
            
           
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

            if len(y)<1500:
                pe_max =  min(80,np.max(y[-400:]))
                pe_mean = min(40,np.mean(y[-400:]))
                pe_min =  np.min(y[-400:])
            else:
                pe_max =  min(80,np.max(y[-1600:]))
                pe_mean = min(40,np.mean(y[-1600:]))
                pe_min =  max(0,np.min(y[-1600:]))
            pe_expect = (0.7*y[-1] + 0.3*pe_mean)
            price_max = np.max(yk[-120:])
            price_min = np.min(yk[-120:])
            if self.industry_dic[self.document['code']][1] in ['银行']:
                jiagetidu = np.array([1+0.01*i for i in range(0,3,1)])
            else:
                jiagetidu = np.array([1+0.035*i for i in range(0,3,1)])

            #过年要改年份
            fenhong = searchHongli(self.document['code'], 2019)
            if fenhong.empty:
                fenhong = searchHongli(self.document['code'], 2018)
                if fenhong.empty:
                    # print('抠门公司无分红->')
                    continue
            try:
                float(fenhong.values[0][-2])
            except:
                continue
            #     else:
            #         print('年份:2018',fenhong.values[0])
            #         print('股息率%.2f%%,%s'%(100*float(fenhong.values[0][-2])/yk[-1], fenhong.values[0][3]),'当前股价:',yk[-1])
            # else:
            #     print('年份:2019',fenhong.values[0])
            #     print('股息率%.f%%,%s'%(100*float(fenhong.values[0][-2])/yk[-1], fenhong.values[0][3]),'当前股价:',yk[-1])

            
            kaocha_day = min(700,len(yk))
            yk_dapan_sub = yk_dapan[-kaocha_day:]
            yk_sub = yk[-kaocha_day:]
            ab = np.array([yk_dapan_sub, yk_sub])
            cor = np.corrcoef(ab)
            xiangguandu += [cor[1][0]]
            additional = ''
            if cor[1][0] > 0.1 :
                if (np.mean(yROE[-5:]) < 15 or (y[-1]-pe_min)/(pe_max-pe_min)*100//1 > 15):
                    pass
                    # continue
                else:
                    pass
                    # additional = '\n股价随大盘波动较大'
                    # continue#
                    
                    # if 100*(yk[-1]/((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1])-1) > 10:
                    #     continue
                    
            else:
                pass
                # if 100*(yk[-1]/((price_min+pe_min*yk[-1]/y[-1])/2*jiagetidu[-1])-1) > 15:
                #     continue
                # continue
                
            if y[-1] > 40:
                additional += "\n该股pe过40，不建议买入"
                continue
            if self.industry_dic[self.document['code']][1] in ['银行', '非银金融'] and y[-1] >2:
                additional += "\n该股pb过2，不建议买入"
                continue

            #test
            # print(code+','+self.industry_dic[self.document['code']][0]+','+self.industry_dic[self.document['code']][1]+','+'申万一级行业')

            guzhi_zhibiao = (y[-1]-pe_min)/(pe_max-pe_min)*100
            guzhi_zhibiao_mean = (pe_mean-pe_min)/(pe_max-pe_min)*100
            dangqianzhangfu_zhibiao_lim = 10
            defence_zhibiao_lim = 95
            expect_Nianhua_lim = 14
            # guzhi_zhibiao_mean = 101#不注释则打开价值因子投资开关
            # dangqianzhangfu_zhibiao_lim = 50#不注释则打开价值因子投资开关
            # defence_zhibiao_lim = 0#不注释则打开价值因子投资开关
            # expect_Nianhua_lim = 14#不注释则打开价值因子投资开关
            expect_Nianhua0 = 100*(( pe_expect/y[-1]*((1+growth)**3))**0.33-1)
            expect_Nianhua = 100*growth
            expect_Jiage = yk[-1] * (1+expect_Nianhua0/100)**3
            lirun_zhibiao = max(shizhi.values())//1e8
            defence_zhibiao = (1 - cor[1][0])*100
            PEG=y[-1]/100/growth
            if self.industry_dic[self.document['code']][1] in ['银行', '非银金融']:
                PEG = 0.8
            dangqianzhangfu_zhibiao = 100*(yk[-1]/((price_min*0.55+0.45*pe_min*yk[-1]/y[-1])*jiagetidu[-1])-1)
            guxilv_zhibiao = 100*float(fenhong.values[0][-2])/yk[-1]
            if False or \
                (guzhi_zhibiao < guzhi_zhibiao_mean and expect_Nianhua > expect_Nianhua_lim and lirun_zhibiao > 1 \
                and dangqianzhangfu_zhibiao < dangqianzhangfu_zhibiao_lim and defence_zhibiao > defence_zhibiao_lim and PEG < 1.5):

                outstr = ' '.join([self.industry_dic[self.document['code']][0],\
                    self.industry_dic[self.document['code']][1],\
                    str(lirun_zhibiao),'亿利润, 价估:%.2f %%'%((y[-1]-pe_min)/(pe_max-pe_min)*100),\
                    "\n当前价格<%s:%.2f元>,"%(max(kline.keys()),yk[-1]),\
                    "\n买入估值参考:",str(pe_min*yk[-1]/y[-1]*jiagetidu*100//1/100),\
                    "\n买入价格参考:",str(price_min*jiagetidu*100//1/100),\
                    "\n买入平均参考:",str((price_min*0.6+0.4*pe_min*yk[-1]/y[-1])*jiagetidu*100//1/100),\
                    # "\n卖出估值保守:",str(pe_mean*yk[-1]/y[-1]*jiagetidu*100//1/100),\
                    # "\n卖出价格保守:",str(price_max*jiagetidu*100//1/100),\
                    # "\n卖出估值激进:",str(pe_max*yk[-1]/y[-1]*jiagetidu*100//1/100),\
                    "\n3年平均杜邦ROE %.2f%%"%(np.mean(yROE[-3:])),\
                    "\n当前PE(B)TTM=%.2f,预计PE(B)=%.2f, peg:%.2f"%(y[-1],0.8*pe_max,PEG), \
                    "\n预计利润增长率=%.2f%%~%.2f%%-%.2f%%-%.2f%%"%(100*growth,100*growth0,100*min(0.25, y2g),100*min(0.25, y1g)), \
                    "\n现在买入预计年化收益=%.2f%%"%(expect_Nianhua0), \
                    '\n股息率%.2f%%,上次分红日期:%s'%(guxilv_zhibiao, fenhong.values[0][3]),\
                    "\n捡钱价建仓参考: %.2f￥, 当前涨幅%.2f%%"%((price_min*0.55+0.45*pe_min*yk[-1]/y[-1])*jiagetidu[-1], dangqianzhangfu_zhibiao),\
                    "\n防御力(越大越好,优质股基准为90%%):%.2f%% %s"%((1 - cor[1][0])*100, additional),\
                    '\n'])

                #test
                # print(code+','+self.industry_dic[self.document['code']][0]+','+self.industry_dic[self.document['code']][1]+','+'申万一级行业')
                # continue
                if dangqianzhangfu_zhibiao < 10:
                    outstr += '可以关注买入'

                stock_list += [(expect_Nianhua,#收益估计
                                self.industry_dic[self.document['code']][0],#名字
                                self.industry_dic[self.document['code']][1],#行业
                                lirun_zhibiao,#利润
                                dangqianzhangfu_zhibiao,#涨幅
                                (1 - cor[1][0])*100,
                                additional,
                                expect_Jiage,
                                yk[-1],
                                100*float(fenhong.values[0][-2])/yk[-1],
                                100*growth,
                                y[-1],
                                PEG,
                                outstr)]#杂项
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
                plt.title('PEorPB_' + 'PEG=' + str(PEG))
                plt.plot(x, [pe_mean for i in range(len(y))])
                plt.plot(x, [pe_max for i in range(len(y))])
                plt.plot(x, [pe_min for i in range(len(y))])
                plt.plot(x, [pe_expect for i in range(len(y))], 'y--')
                

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
                plt.title('Net Profits Value, growth = %.2f%%'%(100*(growth)))
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
                plt.title('yk'+ str(kaocha_day) + 'nianhua=%.2f%%'%(expect_Nianhua0))

                plt.show()
        return stock_list
                
def industryClassifer(stock_list):
    stock_list = sorted(stock_list, key=lambda s: s[0], reverse = True)
    output_stack = {}
    # stock_list += [(#收益估计0,#名字1,#行业2,#利润3,#涨幅4,#杂项5)]
    for item in stock_list:
        try:
            output_stack[item[2]] += [(item)]
        except KeyError:
            output_stack[item[2]] = [(item)]
    j = 0
    i = 0
    print("房地产\"利\"需要大于100亿")
    for key in output_stack.keys():
        output_stack[key] = sorted(output_stack[key], key=lambda s: s[3], reverse = True)
        j+=1
        # i = 0
        print('-------------------------------')
        for item in output_stack[key]:
            i += 1
            try:
                print('%2d-%2d'%(j,i) + ' 成长%.2d%% %s %s 利%.0f亿 攻%.2f%% 防%.2f%% %s 现价%.2f￥ 股息率%.2f%% pe=%.2f PEG=%.2f'\
                            %(item[0],item[1],item[2],item[3],100 - item[4],item[5], item[6], item[8], item[9], item[11], item[12]))
                # print('%2d-%2d'%(j,i) + "%s,建仓价格:%s,-5%%=%.2f￥,-10%%=%.2f￥,建仓日期%s"%(item[1],item[8],0.95*item[8],0.9*item[8],datetime.now().strftime("%Y-%m-%d")))
                # print(item[-1])
                # print(' ')
            except:
                pass

if __name__ == '__main__':
    # stock = stockFeature('./data/stock_industry_select727.csv')
    stock = stockFeature('./data/stock_industry_select915.csv')
    
    # stock.setupDateStore()
    stock.updateStore(datetime.now().strftime("%Y-%m-%d"))
    stock_list = stock.peAnalyse(datetime.now().strftime("%Y-%m-%d"))
    industryClassifer(stock_list)
    print('================')
    # https://www.touzid.com/indice/fundamental.html#/sh000300
    