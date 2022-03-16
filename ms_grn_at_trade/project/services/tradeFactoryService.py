# -*- coding: utf-8 -*-

from locale import currency
import requests
import json
from transitions import Machine, State
from project.models import models
import enum
import uuid


class TradeFactoryService(object):
    def __init__(self, mReqSvc):
        self.myReqSvc = mReqSvc
        pass

    def CreateTrade(self, pbp, psp, tsp, ttp, sp):
        return TradeState(self.myReqSvc, pbp, psp, tsp, ttp, sp)


class States(enum.Enum):
    TRACE_BUY = 0
    BUY_DONE = 1
    SELL_STANDBY = 2
    TRACE_SELL = 3
    SELL_DONE = 4
    CANCEL_SELL = 5
    STOP_LOSS = 6
    CANCEL_ORDER = 7
    ORDER_DONE = 8


class TradeState(Machine):

    # pbp : predictBuyPrice,
    # psp : predictSellPrice,
    # tsp : trailingStopPercent,
    # ttp : trailingTrigerPercent,
    # sp : stoplossPercent,
    # balance : initialize balanace (KRW)
    def __init__(self, mMarket, ticker, balance, pbp, psp, tsp, ttp, sp):
        self.myUuid = uuid.uuid4()
        self.myModel = models.TradeStateModel(
            self.myUuid, ticker, balance, pbp, psp, tsp, ttp, sp)
        self.myReqModule = mMarket
        self.myOrders = []

        self.mMarket = mMarket
        self.buyQty = 0
        self.sellQty = 0
        self.buyPrice = 0
        self.sellPrice = 0
        self.currentPrice = 0
        self.trailStartPrice = 0
        self.trailStopPrice = 0
        self.stopLossPrice = 0

        transitions = [
            {'trigger': 'proceed', 'source': States.TRACE_BUY,
                'dest': States.BUY_DONE, 'before': 'set_environment',
                'conditions': 'is_arrive_predict_buy_price'
             },
            
            {'trigger': 'proceed', 'source': States.BUY_DONE,
                'dest': States.SELL_STANDBY, 'before': 'set_environment',
                'conditions': 'is_arrive_predict_buy_price'
            },
 
            {'trigger': 'proceed', 'source': States.SELL_STANDBY,
                'dest': States.TRACE_SELL, 'before': 'set_environment',
                'conditions': 'is_arrive_stanby_sell_trace'
            },
            
            {'trigger': 'proceed', 'source': States.TRACE_SELL,
                'dest': States.SELL_DONE, 'before': 'set_environment',
                'conditions': 'is_arrive_stanby_sell_done'
            },
            
            {'trigger': 'proceed', 'source': [States.SELL_STANDBY, States.TRACE_SELL], 
                'dest': States.STOP_LOSS, 'before':'set_environment',
                'conditions': 'is_arrive_stoploss'
            },
            
            {'trigger': 'proceed', 'source': States.SELL_DONE,
                'dest': States.ORDER_DONE, 'before': 'set_environment'},
            
            {'trigger': 'user_cancel', 'source': States.TRACE_BUY,
                'dest': States.CANCEL_ORDER, 'before': 'set_environment'},
            
            {'trigger': 'user_cancel', 'source': [States.BUY_DONE, States.SELL_STANDBY,
                                                  States.TRACE_SELL], 'dest': States.CANCEL_SELL, 'before':'set_environment'},
            
            {'trigger': 'proceed', 'source': [States.STOP_LOSS, States.CANCEL_ORDER,
                                              States.CANCEL_SELL], 'dest': States.ORDER_DONE, 'before':'set_environment'},
        ]

        Machine.__init__(self, states=States, initial=States.TRACE_BUY,
                         transitions=transitions, send_event=True)

    def set_environment(self, event):
        pass

    def is_arrive_predict_buy_price(self, event):
        self.currentPrice = event.kwargs.get('currentPrice', self.currentPrice)
        return self.myModel.predictBuyPrice <= self.currentPrice

    def on_enter_TRACE_BUY(self, event):
        self.myModel.trade_state = self.state

    def on_enter_BUY_DONE(self, event):
        res = self.mMarket.buyMarketPrice(self.myModel.ticker, self.myModel.balance);

        self.buyQty = res["executed_volume"]
        self.buyPrice = res["avgPrice"]
        self.myModel.trade_state = self.state
        
        order = models.OrderIdModel();
        order.orderId = res['order-id']
        order.orderType = "buy"
        order.uuid = self.myModel.uuid;
        
        self.myOrders.append(order);

    def on_exit_BUY_DONE(self, event):
        # Todo
        pass
    
    def is_arrive_predict_sell_stand_by(self, event):
        # Todo 
        # Check Qty 
        # But, do trade market price
        pass 
    
    def is_arrive_stanby_sell_trace(self, event):
        self.currentPrice = event.kwargs.get('currentPrice', self.currentPrice)
        return self.trailStartPrice <= self.currentPrice

    def is_arrive_stanby_sell_done(self, event):
        self.currentPrice = event.kwargs.get('currentPrice', self.currentPrice)
        return self.trailStopPrice <= self.currentPrice

    def on_enter_SELL_STANDBY(self, event):
        self.myModel.trade_state = self.state
        self.trailStartPrice = self.buyPrice * (1 + (0.01 * self.myModel.trailingTriggerPercent));
        self.trailStopPrice = self.buyPrice * (1+ (0.01 * (self.myModel.trailingTriggerPercent + self.myModel.trailingStopPercent)));
            
        self.trailStartPrice = self.mMarket.alignPrice(self.trailStartPrice);
        self.trailStopPrice = self.mMarket.alignPrice(self.trailStopPrice);    

        self.stopLossPrice = self.buyPrice * (1 - (0.01 * self.myModel.stoplossPercent))
        self.stopLossPrice = self.mMarket.alignPrice(self.stopLossPrice)

    def on_enter_SELL_TRACE(self, event):
        # Todo 
        self.myModel.trade_state = self.state

    def on_enter_SELL_DONE(self, event):
        self.myModel.trade_state = self.state
        res = self.mMarket.sellMarketPrice(self.myModel.ticker, self.buyQty);
        
        self.sellPrice = res['avgPrice']
        self.sellQty = res['executed_volume']
                
        order = models.OrderIdModel();
        order.orderId = res['order-id']
        order.orderType = "sell"
        order.uuid = self.myModel.uuid;
        
        self.myOrders.append(order);
        pass 
    
    def is_arrive_stoploss(self, event):
        self.currentPrice = event.kwargs.get('currentPrice', self.currentPrice)
        return self.stopLossPrice >= self.currentPrice
    
    def on_enter_STOP_LOSS(self, event):
        self.myModel.trade_state = self.state
    
    def on_etner_ORDER_DONE(self, event):
        self.myModel.trade_state = self.state
        