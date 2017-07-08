from poloniex import Poloniex
from time import time,sleep

import pandas as pd



def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')



pd.set_option('display.width', 300)
polo = Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7',jsonNums=float)
coin = "BTC_DASH"

period = polo.MINUTE * 5



window_short = 8
window_long = 6
SDP = 0.11
SDN = -0.73
buying = -1

print(coin)
while(1):
    df=pd.DataFrame(polo.returnChartData(coin,period,time()-polo.HOUR*6))
    df['date'] = df['date']+polo.DAY/3  #shift time to UTC+8
    df['date'] = pd.to_datetime(df["date"], unit='s')


    df['short'] = pd.ewma(df['close'],com= window_short )
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
    df_last = df.iloc[-1,:]
    # print(df_last)
    sleep(1)

    trade_amount = pd.DataFrame(polo.returnTradableBalances())
    trade_amount = trade_amount[coin]
    DASH = float(trade_amount.DASH)
    BTC = float(trade_amount.BTC)
    order_book = pd.DataFrame(polo.returnOrderBook(coin, 10))
    if (df_last.trade == -2 )&(buying != 0): #sell
        polo.closeMarginPosition(coin)

        polo.marginSell(coin,float(order_book.bids[2][0]),DASH,2)
        buying = 0
        print("Sell at %f" %float(order_book.bids[2][0]) )
    elif (df_last.trade == 2) & (buying != 1):#buy
        polo.closeMarginPosition(coin)
        polo.marginBuy(coin, float(order_book.asks[2][0]), BTC/float(order_book.asks[2][0]), 2)
        buying = 1
        print("buy at %f" %(float(order_book.bids[2][0])))

