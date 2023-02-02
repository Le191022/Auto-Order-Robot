import requests
import datetime
import pandas as pd

'''
#request_url = "https://data.binance.com/api/v3/klines?symbol=ETHBUSD&interval=1m&limit=14"
K线间隔:

s -> 秒; m -> 分钟; h -> 小时; d -> 天; w -> 周; M -> 月

1s
1m
3m
5m
15m
30m
1h
2h
4h
6h
8h
12h
1d
3d
1w
1M
'''

def get_candles(_resolution, _limit):
    request_url = 'https://data.binance.com/api/v3/klines?symbol=ETHBUSD&interval={0}&limit={1}'.format(_resolution,_limit)

    try:
        resp  = requests.get(request_url) 
        resp_json = resp.json()
        #print(resp_json)
        candles_rev = []
        for ml in resp_json:  #把LIST轉成DICT
            st = datetime.datetime.fromtimestamp(ml[0]/1000).isoformat()
            tmp = {'startedAt': st, 'open': ml[1], 'high':  ml[2], 'low': ml[3], 'close':  ml[4]}
            candles_rev.append(tmp)
        #print(candles_rev)
        return(candles_rev)
    except Exception as e:
        print('\n==== Exception {0} : {1}'.format('[task]', e))

get_candles('1m', 3)

