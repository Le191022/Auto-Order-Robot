from talib import abstract
import threading
import datetime
import time
import sys

import order_dydx as odydx
import strategy_KD as kd
import RobotInfo as rt
import order_binance as obinance
def login():
    ETHEREUM_ADDRESS = rt.ETHEREUM_ADDRESS
    WEB3_PROVIDER_URL = rt.WEB3_PROVIDER_URL
    ETH_PRIVATE_KEY = rt.ETH_PRIVATE_KEY
    odydx.onBoard_dydx( ETHEREUM_ADDRESS, ETH_PRIVATE_KEY, WEB3_PROVIDER_URL)

    #odydx.onBoard_dydx( rt.ETHEREUM_ADDRESS_2, rt.ETH_PRIVATE_KEY_2, rt.WEB3_PROVIDER_URL)

def check():
    #candles = odydx.get_candles('1MIN',14)
    candles = obinance.get_candles('1m',14)
    #kd.show(tsmc)
    buy = kd.check(candles)
    odydx.do_strategy(buy)
    
#(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
def main_func():
    localtime = datetime.datetime.now()
    delta = datetime.timedelta(seconds= 60)
    #startTime = datetime.datetime(localtime.year, localtime.month, localtime.day, localtime.hour, 00, 00) + delta
    startTime = localtime
    login()
    print('\n=====================================================')

    print('startTime : ' + startTime.strftime('%Y-%m-%d %H:%M:%S'))

    flag = 0
    while True:
    
        localtime = datetime.datetime.now()
        if(flag == -1):
            break

        if(localtime >= startTime) :
            check()
            startTime += delta
            flag = 0
        else:
            flag += 1
            time.sleep(1)


t1 = threading.Thread(target = main_func, daemon=True)
t1.start()
#print('t1 Thread started')

user_input = 'null'
prompt = '\nPress q to exit....\n\n'
#print('t1:',t1.is_alive())

while user_input == 'null':
    user_input = input(prompt)
    if (user_input == 'q') or (user_input == 'Q') :
        prompt = '\n User press q ....'
        t1.flag = -1
        sys.exit()
        break
