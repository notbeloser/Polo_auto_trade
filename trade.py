from poloniex import Poloniex
from time import time
import sys
import numpy as np
import matplotlib.dates as md
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
from colorama import Fore, Back, Style
from datetime import datetime

from math import pi
import pandas as pd
from bokeh.plotting import figure, output_file, show,save
from bokeh.layouts import column

pd.set_option('display.width', 300)
#print(Fore.RED + 'some red text'+Style.RESET_ALL)
polo = Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7',jsonNums=float)
coin_pair=['BTC_ETH','BTC_XRP','BTC_LTC','BTC_ZEC','BTC_ETC','BTC_DGB','BTC_BTS','BTC_LBC','BTC_FCT','BTC_ARDR','BTC_STRAT','BTC_NXT','BTC_STR','BTC_DASH'
,'BTC_LSK','BTC_SC','BTC_XEM','BTC_STEEM','BTC_GNT','BTC_XMR','BTC_DOGE','BTC_POT','BTC_SYS','BTC_MAID','BTC_GAME','BTC_BURST','BTC_BCN','BTC_REP','BTC_DCR'
,'BTC_FLDC','BTC_GRC','BTC_EMC2','BTC_VTC','BTC_GNO','BTC_PINK','BTC_RADS','BTC_AMP','BTC_NOTE','BTC_CLAM','BTC_PPC','BTC_NAV','BTC_OMNI','BTC_VIA','BTC_BLK',
'BTC_XCP','BTC_XBC','BTC_VRC','BTC_RIC','BTC_PASC','BTC_BTCD','BTC_EXP','BTC_SBD','BTC_SJCX','BTC_NEOS','BTC_FLO','BTC_BELA','BTC_NAUT','BTC_XPM','BTC_NMC',
'BTC_BCY','BTC_XVC','BTC_BTM','BTC_HUC']

margin_pair=['BTC_ETH','BTC_XRP','BTC_LTC','BTC_BTS','BTC_STR','BTC_FCT','BTC_DASH','BTC_XMR','BTC_DOGE','BTC_MAID','BTC_CLAM']

period = polo.MINUTE * 5
df = [pd.DataFrame()]*len(margin_pair)
p=[figure()]*len(margin_pair)
q=[figure()]*len(margin_pair)
output_file("polo_chart.html", title="Poloniex-即時k線")

window_short = 3
window_long = 5
SDP = 0.2
SDN = -0.6
# for i in range(len(margin_pair)):
for i in range(1):
    print(margin_pair[i])
    df[i]=pd.DataFrame(polo.returnChartData(margin_pair[i],period,time()-polo.DAY))
    df[i]['date'] = df[i]['date']+polo.DAY/3  #shift time to UTC+8
    df[i]['date'] = pd.to_datetime(df[i]["date"], unit='s')


    df[i]['short'] = pd.ewma(df[i]['close'],com= window_short )
    df[i]['long'] = pd.rolling_mean(df[i]['close'], window=window_long)
    df[i]['SD']=(df[i].short - df[i].long) / df[i].long * 100
    df[i]['buy'] = df[i]['SD']>SDP
    df[i]['sell'] = df[i]['SD']< SDN
    df[i]['bs'] = df[i].buy != df[i].sell
    trade_index = df[i][df[i]['bs'] == True].index.tolist()

    df[i].dropna(inplace=True)
    df[i]['trade'] = pd.DataFrame.diff(df[i].buy[trade_index]*1 + df[i].sell[trade_index]*-1)
    df[i]['trade'].fillna(0,inplace=True)
    df[i]=df[i].drop(['buy','sell','bs'],axis=1)
    print(df[i])

    w = (period * 1000) - 5000
    tools = "pan,wheel_zoom,box_zoom,reset,save,hover"

    p[i] = figure(x_axis_type="datetime", tools=tools, plot_width=1000,plot_height=400, title=margin_pair[i])
    p[i].xaxis.major_label_orientation = pi / 4
    p[i].grid.grid_line_alpha = 2
    inc = df[i].close > df[i].open
    dec = df[i].open > df[i].close
    p[i].segment(df[i].date, df[i].high, df[i].date, df[i].low, color="black")

    p[i].vbar(df[i].date[inc], w, df[i].open[inc], df[i].close[inc], fill_color="green", line_color="black")
    p[i].vbar(df[i].date[dec], w, df[i].open[dec], df[i].close[dec], fill_color="red", line_color="black")

    p[i].line(df[i].date,df[i].short,color='yellow')
    p[i].line(df[i].date,df[i].long,color='blue')
    trade_index = df[i][df[i]['trade'] ==2].index.tolist()
    p[i].circle(df[i]['date'][trade_index], df[i]['trade'][trade_index]/2*df[i]['weightedAverage'][trade_index]*0.01 +df[i]['weightedAverage'][trade_index] , color='green')
    trade_index = df[i][df[i]['trade'] ==-2].index.tolist()
    p[i].circle(df[i]['date'][trade_index],
                df[i]['trade'][trade_index] / 2 * df[i]['weightedAverage'][trade_index] * 0.01 +
                df[i]['weightedAverage'][trade_index], color='red')

df_index=df[0].index.tolist()


BTC=1
ETH=0
fee=0
trade_time=0
for i in df_index:
    if df[0].trade[i] == -2 and ETH>0:
        BTC=ETH*df[0]['close'][i] * 0.9975
        fee = fee + ETH*df[0]['close'][i] * 0.0025
        ETH=0
        trade_time = trade_time + 1
    elif df[0].trade[i] == 2 and BTC>0:
        ETH=BTC/df[0]['close'][i]*0.9975
        fee = fee + BTC * 0.0025
        BTC=0
        trade_time=trade_time+1
print("BTC %f ETH %f fee %f trade time %f"%(BTC,ETH,fee,trade_time))
if ETH>0:
    print("Equal BTC %f"%(ETH * df[0].close[i] * 0.9975))
#
# BTC=1
# BTC_lend=0
# BTC_Margin=0
# ETH=0
# ETH_lend=0
# ETH_Margin=0
# trade_time=0
# fee=0
# for i in df_index:
#     if df[0].trade[i] == -2: #open Buy Margin && close sell Margin
#         #sell current ETH
#         if BTC_lend >0:
#             BTC_Margin = ETH_Margin * df[0]['close'][i] * 0.9975
#             BTC=BTC_Margin-BTC_lend
#             BTC_Margin = BTC_lend =0
#         #borrow ETH to sell
#         ETH_lend = BTC/df[0]['close'][i] *1.5
#         ETH_Margin = BTC/df[0]['close'][i] *2.5
#         BTC_Margin = ETH_Margin *df[0]['close'][i]*0.9975
#         trade_time=trade_time+1
#     elif df[0].trade[i] == 2:
#         if ETH_lend >0:
#             ETH_Margin = BTC_Margin /df[0]['close'][i] * 0.9975
#             ETH = ETH_Margin -ETH_lend
#             BTC = ETH*df[0]['close'][i]
#             ETH=0
#         BTC_Margin = BTC*2.5
#         BTC_lend = BTC*1.5
#         ETH_Margin = BTC_Margin / df[0]['close'][i] * 0.9975
#         BTC_Margin=0
#
#         trade_time=trade_time+1
#
# print("BTC %f"%BTC)
# print("ETH %f"%ETH)
#
# if ETH>0:
#     print("Equal BTC %f"%(ETH * df[0].close[i] * 0.9975))
# print("Trade time %d"%trade_time)
# show(column(p[0]))