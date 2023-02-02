from talib import abstract
import pandas as pd

'''
candles = [
{'startedAt': '2023-01-06T01:52:00.000Z', 'updatedAt': '2023-01-06T01:52:25.052Z', 'market': 'ETH-USD', 'resolution': '1MIN', 'low': '1253.9', 'high': '1254.1', 'open': '333', 'close': '1253.9', 'baseTokenVolume': '122.999', 'trades': '41', 'usdVolume': '154238.2355', 'startingOpenInterest': '101672.807'}, 

{'startedAt': '2023-01-06T01:51:00.000Z', 'updatedAt': '2023-01-06T01:51:59.692Z', 'market': 'ETH-USD', 'resolution': '1MIN', 'low': '1253.9', 'high': '1254.3', 'open': '222', 'close': '1254', 'baseTokenVolume': '426.528', 'trades': '95', 'usdVolume': '534910.5586', 'startingOpenInterest': '101910.179'}, 

{'startedAt': '2023-01-06T01:50:00.000Z', 'updatedAt': '2023-01-06T01:50:48.236Z', 'market': 'ETH-USD', 'resolution': '1MIN', 'low': '1254.3', 'high': '1254.4', 'open': '111', 'close': '1254.3', 'baseTokenVolume': '53.135', 'trades': '21', 'usdVolume': '66651.3855', 'startingOpenInterest': '101912.189'}]
'''

    
def check( _candles ):
    #print('\n====== 轉成DataFrame ')
    df = pd.DataFrame(_candles)
    df.set_index("startedAt" , inplace=True)
    #print(df)
    
    #print('\n====== 做成dictionary ')
    
    for k, d in df.items():
       if k == "open":
           open = d
           open.index = pd.to_datetime(open.index)
       elif k == "high":
           high = d
           high.index = pd.to_datetime(high.index)
       elif k == "low":
           low = d
           low.index = pd.to_datetime(low.index)
       elif k == "close":
           close = d 
           close.index = pd.to_datetime(close.index)
    
    tsmc = {
        'open':open.dropna().astype(float),
        'high':high.dropna().astype(float),
        'low':low.dropna().astype(float),
        'close':close.dropna().astype(float),
    }
    
    
    kd_list = []

    #修改參數數值
    kd = abstract.STOCH(tsmc,fastk_period=9, slowk_period=3,slowd_period=3)#.tail(10)

    for i in range(0,len(kd[0])):
        tmp = {}
        if(kd[0][i] == kd[0][i]):
            tmp = {
                    "i": i,
                    "startedAt": _candles[i]['startedAt'],
                    "k": kd[0][i],
                    "d": kd[1][i],
                    "side":""
                  } 

            if(kd[0][i-1] == kd[0][i-1]):
                # （今天的 k > d ）且 （昨天的 k < d） 且 （今天的 k < 30） 時，買入
                #side = True if((kd[0][i] > kd[1][i]) and (kd[0][i-1] < kd[1][i-1]) and (kd[0][i] < 30)) else False
    
                
                if((kd[0][i] > kd[1][i]) and (kd[0][i-1] < kd[1][i-1])):
                    # （今天的 k > d ）且 （昨天的 k < d） 時，買入
                    tmp["side"] = 'Buy'
                elif((kd[0][i] < kd[1][i]) and (kd[0][i-1] > kd[1][i-1])):
                    # （今天的 k < d ）且 （昨天的 k > d） 時，賣出
                    tmp["side"] = 'Sell'

                #side = True if((kd[0][i] > kd[1][i]) and (kd[0][i-1] < kd[1][i-1])) else False
                #tmp["side"] = buy
                
            kd_list.append(tmp)
    return(kd_list)