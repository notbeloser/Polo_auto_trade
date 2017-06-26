from poloniex import Poloniex
from time import time
import sys
import numpy as np
import matplotlib.dates as md
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
from colorama import Fore, Back, Style
from datetime import datetime
from math import pi
import pandas as pd
from bokeh.plotting import figure, output_file, show

pd.set_option('display.width', 200)
#print(Fore.RED + 'some red text'+Style.RESET_ALL)
polo = Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7',jsonNums=float)

coin_pair=['BTC_ETH','BTC_XRP','BTC_LTC','BTC_ZEC','BTC_ETC','BTC_DGB','BTC_BTS','BTC_LBC','BTC_FCT','BTC_ARDR','BTC_STRAT','BTC_NXT','BTC_STR','BTC_DASH'
,'BTC_LSK','BTC_SC','BTC_XEM','BTC_STEEM','BTC_GNT','BTC_XMR','BTC_DOGE','BTC_POT','BTC_SYS','BTC_MAID','BTC_GAME','BTC_BURST','BTC_BCN','BTC_REP','BTC_DCR'
,'BTC_FLDC','BTC_GRC','BTC_EMC2','BTC_VTC','BTC_GNO','BTC_PINK','BTC_RADS','BTC_AMP','BTC_NOTE','BTC_CLAM','BTC_PPC','BTC_NAV','BTC_OMNI','BTC_VIA','BTC_BLK',
'BTC_XCP','BTC_XBC','BTC_VRC','BTC_RIC','BTC_PASC','BTC_BTCD','BTC_EXP','BTC_SBD','BTC_SJCX','BTC_NEOS','BTC_FLO','BTC_BELA','BTC_NAUT','BTC_XPM','BTC_NMC',
'BTC_BCY','BTC_XVC','BTC_BTM','BTC_HUC']
k_line = 50
period = polo.MINUTE * 5
df = [pd.DataFrame()]*len(coin_pair)
# for i in range(len(coin_pair)):
for i in range(2):
    # print(coin_pair[i])
    df[i]=pd.DataFrame(polo.returnChartData(coin_pair[i],period,time()-polo.DAY))
    df[i]['date'] = pd.to_datetime(df[i]["date"], unit='s')
    df[i].dropna(inplace=True)
    w = (period * 1000) - 5000
    tools = "pan,wheel_zoom,box_zoom,reset,save"

    output_file(coin_pair[i]+".html", title=coin_pair[i]+"-Poloniex")

    p = figure(x_axis_type="datetime", tools=tools, plot_width=1500, title=coin_pair[i])
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.7

    inc = df[i].close > df[i].open
    dec = df[i].open > df[i].close

    p.segment(df[i].date, df[i].high, df[i].date, df[i].low, color="black")

    p.vbar(df[i].date[inc], w, df[i].open[inc], df[i].close[inc], fill_color="green", line_color="black")
    p.vbar(df[i].date[dec], w, df[i].open[dec], df[i].close[dec], fill_color="red", line_color="black")

    show(p)






