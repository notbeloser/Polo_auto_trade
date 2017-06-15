import poloniex
import time
import sys
polo = poloniex.Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7')

coin_pair=['BTC_ETH','BTC_XRP','BTC_LTC','BTC_ZEC','BTC_ETC','BTC_DGB','BTC_BTS','BTC_LBC','BTC_FCT','BTC_ARDR','BTC_STRAT','BTC_NXT','BTC_STR','BTC_DASH'
,'BTC_LSK','BTC_SC','BTC_XEM','BTC_STEEM','BTC_GNT','BTC_XMR','BTC_DOGE','BTC_POT','BTC_SYS','BTC_MAID','BTC_GAME','BTC_BURST','BTC_BCN','BTC_REP','BTC_DCR'
,'BTC_FLDC','BTC_GRC','BTC_EMC2','BTC_VTC','BTC_GNO','BTC_PINK','BTC_RADS','BTC_AMP','BTC_NOTE','BTC_CLAM','BTC_PPC','BTC_NAV','BTC_OMNI','BTC_VIA','BTC_BLK',
'BTC_XCP','BTC_XBC','BTC_VRC','BTC_RIC','BTC_PASC','BTC_BTCD','BTC_EXP','BTC_SBD','BTC_SJCX','BTC_NEOS','BTC_FLO','BTC_BELA','BTC_NAUT','BTC_XPM','BTC_NMC',
'BTC_BCY','BTC_XVC','BTC_BTM','BTC_HUC']

"""for a in range(10):
	k=polo.returnChartData(coin_pair[a],300)
	file = open(coin_pair[a]+'_kline','w+')
	
	for i in range(len(k)):
		str="%s,date %d ,open %.8f,close %.8f,high %.8f,low %.8f,quoteVolume %.8f,weightedAverage %.8f\n" %(coin_pair[a],int(k[i]['date']),float(k[i]['open']),float(k[i]['close'])
		,float(k[i]['high']),float(k[i]['low']),float(k[i]['quoteVolume']),float(k[i]['weightedAverage']))
		print(str)
		file.write(str)
	file.close()"""
