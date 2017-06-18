import poloniex
import time
import sys
from colorama import Fore, Back, Style
#print(Fore.RED + 'some red text'+Style.RESET_ALL)
polo = poloniex.Poloniex('GBC146G1-M9RGA0VT-T5FL729B-P8OTN6SU',
'a4d44e8e4e4432e9a9a94d66fb17a7b7081858aaeb85c0fdd9b6ebf8a51a7d2fa0160c5db0e55b8d836ba6d64b1c0e324eba164b94278617edd2eec48c09acb7')

coin_pair=['BTC_ETH','BTC_XRP','BTC_LTC','BTC_ZEC','BTC_ETC','BTC_DGB','BTC_BTS','BTC_LBC','BTC_FCT','BTC_ARDR','BTC_STRAT','BTC_NXT','BTC_STR','BTC_DASH'
,'BTC_LSK','BTC_SC','BTC_XEM','BTC_STEEM','BTC_GNT','BTC_XMR','BTC_DOGE','BTC_POT','BTC_SYS','BTC_MAID','BTC_GAME','BTC_BURST','BTC_BCN','BTC_REP','BTC_DCR'
,'BTC_FLDC','BTC_GRC','BTC_EMC2','BTC_VTC','BTC_GNO','BTC_PINK','BTC_RADS','BTC_AMP','BTC_NOTE','BTC_CLAM','BTC_PPC','BTC_NAV','BTC_OMNI','BTC_VIA','BTC_BLK',
'BTC_XCP','BTC_XBC','BTC_VRC','BTC_RIC','BTC_PASC','BTC_BTCD','BTC_EXP','BTC_SBD','BTC_SJCX','BTC_NEOS','BTC_FLO','BTC_BELA','BTC_NAUT','BTC_XPM','BTC_NMC',
'BTC_BCY','BTC_XVC','BTC_BTM','BTC_HUC']

k_line_amount = 5
for i in range(len(coin_pair)):
	Chart=polo.returnChartData(coin_pair[i],300,time.time()-300*k_line_amount,time.time())
	print(coin_pair[i])
	k_av=[0]*len(Chart)
	for j in range(len(Chart)):
		k_av[j]=float( Chart[len(Chart)-j-1]['weightedAverage'])
	for j in range(len(k_av)):
		k_str ="%.8f" %(k_av[j])
		if j==0:
			print(Fore.GREEN +k_str+Style.RESET_ALL,end="\t")
		elif k_av[j]>=k_av[j-1]:
			print(Fore.GREEN +k_str+Style.RESET_ALL,end="\t")
		else:
			print(Fore.RED +k_str+Style.RESET_ALL,end="\t")
	print("")
	for j in range(len(k_av)):
		if j==0:
			print(Fore.GREEN+"0.00000000%"+Style.RESET_ALL,end="\t")
		elif k_av[j]>=k_av[j-1]:
			percent="%.8f" %((k_av[j]-k_av[j-1])/k_av[j-1]*100)
			print(Fore.GREEN +percent+"%"+Style.RESET_ALL,end="\t")
		else:
			percent="%.8f"%((k_av[j]-k_av[j-1])/k_av[j-1]*100)
			print(Fore.RED + percent+"%"+Style.RESET_ALL,end="\t")

	change =(k_av[len(k_av)-1]-k_av[0])/k_av[0]*100
	change_str = "%.8f"%change
	if change >=0:
		print(Fore.GREEN+"Rising\t"+change_str+"%"+Style.RESET_ALL)
	else:
		print(Fore.RED+"Falling\t"+change_str+"%"+Style.RESET_ALL)

