import json
import math
from shutil import register_unpack_format


class MockMarket():

    def __init__(self):
        self.feeRatio = 0.05
        self.testBuyBtcPrice = 48694000
        self.testBuyEthPrice = 3216000
        self.testSellBtcPrice = 49667000
        self.testSellEthPrice = 3316000
        pass

    def buyMarketPrice(self, ticker, balance):
        price = 0;
        if (ticker == 'KRW-BTC'):
            price = self.testBuyBtcPrice
        elif (ticker == "KRW-ETH"):
            price = self.testBuyEthPrice

        paid_fee = self.calcBuyFee(price, balance)
        return {'avgPrice': price, 'executed_volume': balance, paid_fee: paid_fee, 'order-id': 'cdd92199-2897-4e14-9448-f923320408ad'}

    def sellMarketPrice(self, ticker, qty): 
        price = 0;
        if (ticker == 'KRW-BTC'):
            price = self.testSellBtcPrice
        elif (ticker == "KRW-ETH"):
            price = self.testSellEthPrice
        
        paid_fee = self.calcBuyFee(price, qty)
        return {'avgPrice': price, 'executed_volume': qty, paid_fee: paid_fee, 'order-id': 'cdd92199-2897-4e14-9448-f923320408ad'}
      
      
    def alignPrice(self, price):
        if price >= 2000000:
            tick_size = math.floor(price / 1000) * 1000
        elif price >= 1000000:
            tick_size = math.floor(price / 500) * 500
        elif price >= 500000:
            tick_size = math.floor(price / 100) * 100
        elif price >= 100000:
            tick_size = math.floor(price / 50) * 50
        elif price >= 10000:
            tick_size = math.floor(price / 10) * 10
        elif price >= 1000:
            tick_size = math.floor(price / 5) * 5
        elif price >= 100:
            tick_size = math.floor(price / 1) * 1
        elif price >= 10:
            tick_size = math.floor(price / 0.1) / 10
        else:
            tick_size = math.floor(price / 0.01) / 100

        return tick_size
    def calcBuyFee(self, price, balance):
        return (balance/(self.feeRatio * price)) 
    
    def calcSellFee(self, price, qty):
        return price * qty * (self.feeRatio)
