from dydx3 import Client
from dydx3.constants import API_HOST_MAINNET
from dydx3.constants import NETWORK_ID_MAINNET
from dydx3.constants import ACCOUNT_ACTION_DEPOSIT

from dydx3.constants import MARKET_ETH_USD

from dydx3.constants import ORDER_SIDE_BUY
from dydx3.constants import ORDER_SIDE_SELL
from dydx3.constants import ORDER_STATUS_OPEN

from dydx3.constants import ORDER_TYPE_LIMIT
from dydx3.constants import ORDER_TYPE_MARKET


from web3 import Web3
import time
import datetime


def onBoard_dydx( _eth_address, _eth_private_key, _web3_url):
    try:
        #print(' ethereumAddress : {0} \n'.format(_eth_address))
        #print(' eth_private_key : {0} \n'.format(_eth_private_key))
        #print(' web3_url        : {0} \n'.format(_web3_url))

        global client
        client = Client(
            network_id = NETWORK_ID_MAINNET,
            host = API_HOST_MAINNET,
            default_ethereum_address = _eth_address,
            web3=Web3(Web3.HTTPProvider(_web3_url)),
            eth_private_key = _eth_private_key,
        )
        
        # set Api Key.
        #print('\n===== set Api Key ')
        api_key_response = client.eth_private.create_api_key(
            ethereum_address= _eth_address,
        )
        client.api_key_credentials = api_key_response.data['apiKey']
        #print(api_key_response.data['apiKey'])
        
        
        # Set STARK key.
        #print('\n===== Set STARK key ')
        stark_private_key = client.onboarding.derive_stark_key()
        client.stark_private_key = stark_private_key['private_key']
        #print(stark_private_key)
        
        get_account()
        get_user()
        show_onboard()
        return(client)
    except Exception as e:
        print('\n==== Exception {0} : {1}'.format('[onBoard]', e))


def get_account():
    try:
        #print('\n===== get_accounts')
        global account
        global position_id
        account = client.private.get_account()
        position_id = account.data['account']['positionId']
        #print(account.data)
    except Exception as e:
         print('\n==== Exception {0} : {1}'.format('[get_account]', e))


def get_user():
    try:
        #print('\n=========== get user')
        global user
        user = client.private.get_user()
        #print(user.data['user'])
    except Exception as e:
         print('\n==== Exception {0} : {1}'.format('[get_user]', e))

def show_onboard():
    ethereumAddress = user.data['user']['ethereumAddress']
    quoteBalance = account.data['account']['quoteBalance']
    walletType = user.data['user']['userData']['walletType']
    
    print('==== onboard dydx ==== \n')
    print(' Eth Address   : {0} \n'.format(ethereumAddress))
    print(' Quote Balance : {0:.2f} \n'.format(float(quoteBalance)))
    print(' Wallet Type   : {0} \n'.format(walletType))

def get_candles(_resolution, _limit):
    try:
        #print('\n=========== get candles')
        candles = client.public.get_candles(
            market = MARKET_ETH_USD,
            resolution = _resolution,
            limit = _limit
        )
        candles_rev = candles_rever(candles)
        #print(candles_rev)
        return(candles_rev)
    except Exception as e:
         print('\n==== Exception {0} : {1}'.format('[get_candles]', e))


def candles_rever( _candles):
    #print('\n====== 反轉 candles ')
    rev=[]
    for idx in reversed(_candles.data['candles']):
        rev.append(idx)
    
    #print(rev)
    return(rev)


def order( _side, _size, _sec):

    if(_side == 'Buy'):
        order_side = ORDER_SIDE_BUY 
    elif(_side == 'Sell'):
        order_side = ORDER_SIDE_SELL
    else:
        print('==== order side error !! \n')
        return

    try:
        order_params = {
            'position_id': position_id,
            'market': MARKET_ETH_USD,
            'side': order_side,
            'order_type': ORDER_TYPE_LIMIT,
            'post_only': True,
            'size': _size,
            'price': '1',
            'limit_fee': '0.01',
            'expiration_epoch_seconds': time.time() + (60 * _sec),
        }

        order_response = client.private.create_order(**order_params)
        order_id = order_response.data['order']['id']
        
        result = 'Success' if(len(order_id) > 0) else 'Fail'
        localtime = datetime.datetime.now()

        print('\n==== order  {0}:{1} {2} == {3} \n'.format(_side, _size, result,localtime.strftime('%Y-%m-%d %H:%M:%S')))
        #print(order_response.data)
        print(' side : {0} \n'.format(order_params['side']))
        print(' size : {0} \n'.format(order_params['size']))
        print(' Order Id : {0} \n'.format(order_id))

    except Exception as e:
         print('\n==== Exception {0} : {1}'.format('[order]', e))


def do_strategy(buy):
    for i in range(0,len(buy)):
        print(buy[i])
    
    tag = len(buy) -1
    strategy = buy[tag]['side']
    if(strategy== 'Buy'):
        order( 'Buy', '0.01', 2)
    elif(strategy == 'Sell'):
        order( 'Sell', '0.01', 2)
    else:
        localtime = datetime.datetime.now()
        print('\n==== undo ==== {0} \n'.format(localtime.strftime('%Y-%m-%d %H:%M:%S')))
