import json
from locale import currency
import os
import unittest
from project.services import tradeFactoryService
from project.services.tradeFactoryService import States
from typing import Dict, List, Union, Text
from . import mockMarket


class TradeStateTestCase(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_home(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(200, 200)

    def test_transation_succeed(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=49260000)
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.proceed(currentPrice=49667000)
        self.assertEqual(States.SELL_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_1(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_ORDER, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_2(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_3(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_4(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=49260000)
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_4(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48207000)
        self.assertEqual(States.STOP_LOSS, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)
        
    def test_transation_user_cancel_case_5(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=49180000)
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48207000)
        self.assertEqual(States.STOP_LOSS, testTradeObj.state)

    def test_set_buyPrice(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

    def test_condition_trasition_tracebuy_to_buydone(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockMarket.MockMarket(), "KRW-BTC", 1000000, 48694000, 1, 1, 1, 1)
        testTradeObj.proceed(currentPrice=10)
        self.assertNotEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed(currentPrice=48694000)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)
        self.assertEqual(testTradeObj.buyPrice, 48694000)
        self.assertEqual(testTradeObj.buyQty, 1000000)
        
        testTradeObj.proceed();
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)
        
        self.assertEqual(testTradeObj.trailStartPrice, 49180000)  
        self.assertEqual(testTradeObj.trailStopPrice, 49667000)  
        self.assertEqual(testTradeObj.stopLossPrice, 48207000)  

        testTradeObj.proceed(currentPrice=48307000)
        self.assertNotEqual(States.TRACE_SELL, testTradeObj.state)
        self.assertNotEqual(States.STOP_LOSS, testTradeObj.state)

        testTradeObj.proceed(currentPrice=49180000)
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.proceed(currentPrice=49667000)
        self.assertEqual(States.SELL_DONE, testTradeObj.state)
        
        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)