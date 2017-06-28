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
coin = "BTC_ETH"

period = polo.MINUTE * 5
output_file(coin+".html", title="Poloniex-即時k線")



window_short = 11
window_long = 17
SDP = 0.11
SDN = -0.73


print(coin)
df=pd.DataFrame(polo.returnChartData(coin,period,time()-polo.DAY))
df['date'] = df['date']+polo.DAY/3  #shift time to UTC+8
df['date'] = pd.to_datetime(df["date"], unit='s')


df['short'] = pd.ewma(df['close'],com= window_short ) * 0.995
df['long'] = pd.rolling_mean(df['close'], window=window_long)
df['short_diff'] = df['short'].diff() /df['short'] *100
df['long_diff'] = df['long'].diff() / df['long']*100
df['SD'] = (df.short - df.long)/df.long * 100
df['SD_diff'] = df['SD'].diff()
df['buy'] = df.SD > SDP
df['sell'] = df.SD < SDN
df['bs'] = df.buy != df.sell
trade_index = df[df['bs'] == True].index.tolist()

df.dropna(inplace=True)
df['trade'] = pd.DataFrame.diff(df.buy[trade_index]*1 + df.sell[trade_index]*-1)
df['trade'].fillna(0,inplace=True)
df=df.drop(['buy','sell','bs'],axis=1)
# print(df)

w = (period * 1000) - 5000
tools = "pan,wheel_zoom,box_zoom,reset,save,hover"

p = figure(x_axis_type="datetime", tools=tools, plot_width=1000,plot_height=400, title=coin)
p.xaxis.major_label_orientation = pi / 4
p.grid.grid_line_alpha = 2
inc = df.close > df.open
dec = df.open > df.close
p.segment(df.date, df.high, df.date, df.low, color="black")

p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="green", line_color="black")
p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="red", line_color="black")

p.line(df.date,df.short,color='yellow')
p.line(df.date,df.long,color='blue')

trade_index = df[df['trade'] ==2].index.tolist()
p.circle(df['date'][trade_index], df['trade'][trade_index]/2*df['weightedAverage'][trade_index]*0.01 +df['weightedAverage'][trade_index] , color='blue')
trade_index = df[df['trade'] ==-2].index.tolist()
p.circle(df['date'][trade_index],
            df['trade'][trade_index] / 2 * df['weightedAverage'][trade_index] * 0.01 +
            df['weightedAverage'][trade_index], color='black')

df_index=df.index.tolist()

#test profit
BTC=1
BTS=0
fee=0
trade_time=0
for i in df_index:
    if df.trade[i] == -2 and BTS>0:
        BTC=BTS*df['close'][i] * 0.9975
        fee = fee + BTS*df['close'][i] * 0.0025
        BTS=0
        trade_time = trade_time + 1
    elif df.trade[i] == 2 and BTC>0:
        BTS=BTC/df['close'][i]*0.9975
        fee = fee + BTC * 0.0025
        BTC=0
        trade_time=trade_time+1
print("BTC %f EMC2 %f fee %f trade time %f"%(BTC,BTS,fee,trade_time))
if BTS>0:
    print("Equal BTC %f"%(BTS * df.close[i] * 0.9975))


show(column(p))