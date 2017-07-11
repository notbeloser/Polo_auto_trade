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


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


polo = Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7',jsonNums=float)
coin = "BTC_MAID"

period = polo.MINUTE * 5
out=[]



df=pd.DataFrame(polo.returnChartData(coin,period,time()-polo.DAY*7))
df['date'] = df['date'] + polo.DAY / 3  # shift time to UTC+8
df['date'] = pd.to_datetime(df["date"], unit='s')

window_short = 8
window_long = 6

SDP = 0.262626
SDN= -0.232323

index = 0
print(coin)

for SDN in np.linspace(-1,0,101):
    for SDP in np.linspace(0,1,101):
        for window_short in range(3,11):
            for window_long in range(3,21):
                df['short'] = pd.ewma(df['weightedAverage'], com=window_short)
                df['long'] = pd.rolling_mean(df['weightedAverage'], window=window_long)
                df['short_diff'] = df['short'].diff() / df['short'] * 100
                df['long_diff'] = df['long'].diff() / df['long'] * 100
                df['SD'] = (df.short - df.long) / df.long * 100
                df['SD_diff'] = df['SD'].diff()

                df['buy'] = df.SD > SDP
                df['sell'] = df.SD < SDN
                df['bs'] = df.buy != df.sell
                trade_index = df[df['bs'] == True].index.tolist()

                df.dropna(inplace=True)
                df['trade'] = pd.DataFrame.diff(df.buy[trade_index]*1 + df.sell[trade_index]*-1)
                df['trade'].fillna(0,inplace=True)
                # df=df.drop(['buy','sell','bs'],axis=1)
                # print_full(df)


                df_index=df.index.tolist()

                #test profit
                BTC = 1
                fee = 0
                trade_state = 0 #0 is buy 1 is sell
                last_price = 0
                trade_time=0
                win =0
                lose =0
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
                    elif df.trade[i] == 2 :
                        if last_price>0:
                            if last_price*0.9975 > df['close'][i] :
                                win = win+1
                            else:
                                lose = lose +1

                            fee = last_price / df['close'][i] * BTC * 0.0025 + fee
                            BTC = last_price / df['close'][i] * BTC * 0.9975
                        last_price = df['close'][i]
                        trade_time=trade_time+1

                try:
                    win_rate = win / trade_time * 100
                except:
                    win_rate = 0
                print("BTC %f fee %f trade time %d win %d lose %d,win rate %f,SDN %f,SDP %f,window short %d,window long %d"%(BTC,fee,trade_time,win,lose,win_rate,SDN,SDP,window_short,window_long))
                out.append([BTC,fee,trade_time,win,lose,win_rate,SDN,SDP,window_short,window_long])

out_df = pd.DataFrame(out,columns=["BTC","fee","trade time","win","lose","win rate","SDN","SDP","window short","window long"])
out_df = out_df.sort_values('BTC',ascending=False)
print_full(out_df)