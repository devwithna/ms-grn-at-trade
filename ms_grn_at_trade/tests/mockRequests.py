import json
from shutil import register_unpack_format 

class MockRequests():
    
    def __init__(self):
        pass
    
    def get(self, msg):
        if 'buy_market_order' in msg:
            params = self.parseMarketParam(msg);
            
            ticker = params[0]
            balance = params[1]
            
            if (ticker == 'KRW-BTC'):
                btcPrice = 1432
                fee = 0.05
                qty = round((int(balance)/(1+fee)) / btcPrice, 2)
                
                return {'avgPrice': btcPrice, 'qty': qty, 'order-id': 'cdd92199-2897-4e14-9448-f923320408ad'}
            elif (ticker == "KRW-ETH"):
                ethPrice = 143
                fee = 0.05
                qty = round((balance/(1+fee)) / ethPrice, 2)
                
                return {'avgPrice': ethPrice, 'qty': qty, 'order-id': 'cdd92199-2897-4e14-9448-f923320408ad'}
        elif 'sell_market_order' in msg:
            params = self.parseMarketParam(msg);
            
            ticker = params[0]
            qty = params[1]
            
            if (ticker == 'KRW-BTC'):
                btcPrice = 1332
                fee = 0.05
                paid_fee = (btcPrice * qty) * (fee)
                
                return {'avgPrice': btcPrice, 'qty': qty, paid_fee:paid_fee, 'order-id': 'cdd92199-2897-4e14-9448-f923320408ae'}
            elif (ticker == "KRW-ETH"):
                btcPrice = 1332
                fee = 0.05
                paid_fee = (btcPrice * qty) * (fee)
                
                return {'avgPrice': btcPrice, 'qty': qty, paid_fee:paid_fee, 'order-id': 'cdd92199-2897-4e14-9448-f923320408ae'}
            
    def parseMarketParam(self, rawParam):
        rawParams = rawParam.split('?')
        
        resParams = []
        params = rawParams[1].split('&')
        for param in params:
            resParams.append(param.split('=')[1])
            
        return resParams