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

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

pd.set_option('display.width', 300)
polo = Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7',jsonNums=float)
coin = "BTC_MAID"

period = polo.MINUTE * 5
output_file(coin+".html", title="Poloniex-即時k線")



window_short = 11
window_long = 18

SDP = 0.262626
SDN= -0.232323
RSI_DAY = 9
df=pd.DataFrame(polo.returnChartData(coin,period,time()-polo.DAY*1))
index = 0
print(coin)
df['date'] = df['date'] + polo.DAY / 3  # shift time to UTC+8
df['date'] = pd.to_datetime(df["date"], unit='s')
df['short'] = pd.ewma(df['close'], span=window_short)
df['long'] = pd.rolling_mean(df['close'], window=window_long)

df['short_diff'] = df['short'].diff() / df['short'] * 100
df['long_diff'] = df['long'].diff() / df['long'] * 100
df['DIF'] = pd.ewma(df['weightedAverage'], span=12) - pd.ewma(df['weightedAverage'], span=26)
df['DEM'] = pd.ewma(df['DIF'], span=9)
df['OSC'] = df.DIF - df.DEM
df['OSC_signal'] = (df['OSC'] >= 0) *1

df['std'] = pd.rolling_std(df['close'],window=window_long)
df['bl_up'] = df['long'] + df['std']*2
df['bl_down'] = df['long'] - df['std']*2

df['close_diff'] = df['close'].diff()

inc = df['close_diff'] >= 0
dec = df['close_diff'] < 0
df['U'] = df['close_diff'][inc]
df['D'] = abs(df['close_diff'][dec])
df['U_EMA'] = pd.ewma(df['U'],span=RSI_DAY,ignore_na=True)
df['D_EMA'] = pd.ewma(df['D'],span=RSI_DAY,ignore_na=True)
df['RSI'] = df['U_EMA'] / (df['U_EMA']+df['D_EMA']) * 100

df['buy'] = df['OSC_signal'].diff()  == 1
df['sell'] = df['OSC_signal'].diff()  == -1
df['bs'] = df.buy != df.sell
trade_index = df[df['bs'] == True].index.tolist()

# df.dropna(inplace=True)
df['trade'] = pd.DataFrame.diff(df.buy[trade_index]*1 + df.sell[trade_index]*-1)
df=df.drop(['buy','sell','bs'],axis=1)
df['trade'].fillna(0,inplace=True)

print_full(df)
# print(df)
w = (period * 1000) - 5000
tools = "pan,wheel_zoom,box_zoom,reset,save,hover"

p = figure(x_axis_type="datetime", tools=tools, plot_width=1200,plot_height=500, title=coin)
p.xaxis.major_label_orientation = pi / 4
p.grid.grid_line_alpha = 2
inc = df.close > df.open
dec = df.open > df.close
p.segment(df.date, df.high, df.date, df.low, color="black")

p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="green", line_color="black")
p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="red", line_color="black")

p.line(df.date,df.short,color='yellow')
p.line(df.date,df.long,color='blue')

p.line(df.date,df.bl_up,color='black')
p.line(df.date,df.bl_down,color='black')


trade_index = df[df['trade'] ==2].index.tolist()
p.circle(df['date'][trade_index],df['close'][trade_index],color='blue')
trade_index = df[df['trade'] ==-2].index.tolist()
p.circle(df['date'][trade_index],df['close'][trade_index],color='black')

df_index=df.index.tolist()

p1 = figure(x_axis_type="datetime", tools=tools, plot_width=1200,plot_height=200, title=coin)
p1.xaxis.major_label_orientation = pi / 4
p1.grid.grid_line_alpha = 2
inc = df.OSC_signal == 1
dec = df.OSC_signal == 0
p1.vbar(df.date[inc], w, 0, df.OSC[inc], fill_color="green", line_color="black")
p1.vbar(df.date[dec], w, 0, df.OSC[dec], fill_color="red", line_color="black")
p1.line(df.date,df.DEM,color='yellow')
p1.line(df.date,df.DIF,color='blue')

p2 = figure(x_axis_type="datetime", tools=tools, plot_width=1200,plot_height=200, title=coin)
p2.xaxis.major_label_orientation = pi / 4
p2.grid.grid_line_alpha = 2
p2.line(df.date,df.RSI,color='blue')
p2.line(df.date,30,color='black')
p2.line(df.date,70,color='black')

#test profit
BTC = 1
fee = 0
trade_state = 0 #0 is buy 1 is sell
last_price = 0
trade_time=0
win =0
lose =0
buying = -1
stop_loss=0
for i in df_index:
    if df.trade[i] == -2 :
        if last_price>0:
            fee = df['close'][i]/ last_price * BTC * 0.0025 +fee
            BTC = df['close'][i]/ last_price * BTC * 0.9975
            if last_price < df['close'][i]*0.9975 :
                win = win+1
            else:
                lose = lose +1
        last_price = df['close'][i]
        trade_time=trade_time+1
        buying = 0
    if df.trade[i] == 2 :
        if last_price>0:
            if last_price*0.9975 > df['close'][i] :
                win = win+1
            else:
                lose = lose +1

            fee = last_price / df['close'][i] * BTC * 0.0025 + fee
            BTC = last_price / df['close'][i] * BTC * 0.9975
        last_price = df['close'][i]
        trade_time=trade_time+1
        buying = 1

    # if buying == 1:
    #     if df['close'][i]/last_price < 0.97  :
    #         BTC=df['close'][i] / last_price * 0.9975 * BTC
    #         buying = -1
    #         last_price = 0
    #         p.circle(df['date'][i], df['close'][i], color='yellow')
    #         stop_loss=stop_loss+1
    # elif buying == 0:
    #     if last_price / df['close'][i] < 0.97:
    #         BTC=last_price / df['close'][i] * 0.9975 * BTC
    #         buying = -1
    #         last_price = 0
    #         p.circle(df['date'][i], df['close'][i], color='yellow')
    #         stop_loss=stop_loss+1


try:
    win_rate = win / trade_time * 100
except:
    win_rate = 0
print("BTC %f fee %f trade time %d win %d lose %d,stop loss %d,win rate %f,SDN %f,SDP %f"%(BTC,fee,trade_time,win,lose,stop_loss,win_rate,SDN,SDP))

show(column(p,p1,p2))