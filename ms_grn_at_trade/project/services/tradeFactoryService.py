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
    def __init__(self, mReq, ticker, balance, pbp, psp, tsp, ttp, sp):
        self.myUuid = uuid.uuid4()
        self.myModel = models.TradeStateModel(
            self.myUuid, ticker, balance, pbp, psp, tsp, ttp, sp)
        self.myReqModule = mReq

        self.mReq = mReq
        self.quantity = 0
        self.buyPrice = 0
        self.sellPrice = 0
        self.currentPrice = 0

        transitions = [
            {'trigger': 'proceed', 'source': States.TRACE_BUY,
                'dest': States.BUY_DONE, 'before': 'set_environment',
                'conditions': 'is_arrive_predict_buy_price'
             },
            {'trigger': 'proceed', 'source': States.BUY_DONE,
                'dest': States.SELL_STANDBY, 'before': 'set_environment'},
            {'trigger': 'proceed', 'source': States.SELL_STANDBY,
                'dest': States.TRACE_SELL, 'before': 'set_environment'},
            {'trigger': 'proceed', 'source': States.TRACE_SELL,
                'dest': States.SELL_DONE, 'before': 'set_environment'},
            {'trigger': 'proceed', 'source': States.SELL_DONE,
                'dest': States.ORDER_DONE, 'before': 'set_environment'},
            {'trigger': 'user_cancel', 'source': States.TRACE_BUY,
                'dest': States.CANCEL_ORDER, 'before': 'set_environment'},
            {'trigger': 'user_cancel', 'source': [States.BUY_DONE, States.SELL_STANDBY,
                                                  States.TRACE_SELL], 'dest': States.CANCEL_SELL, 'before':'set_environment'},
            {'trigger': 'stoploss', 'source': [
                States.SELL_STANDBY, States.TRACE_SELL], 'dest': States.STOP_LOSS, 'before':'set_environment'},
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

    def on_exit_TRACE_BUY(self, event):
        res = self.mReq.get(
            "buy_market_order?ticker=KRW-BTC&volume=" + str(self.myModel.balance))

        self.quantity = res["qty"]

        self.buyPrice = res["avgPrice"]
