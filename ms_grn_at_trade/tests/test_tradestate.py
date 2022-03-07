import json
from locale import currency
import os
import unittest
from project.services import tradeFactoryService
from project.services.tradeFactoryService import States
from typing import Dict, List, Union, Text
from . import mockRequests


class TradeStateTestCase(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_home(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(200, 200)

    def test_transation_succeed(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=1)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_1(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_ORDER, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_2(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=1)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_3(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=1)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_4(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=1)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.user_cancel()
        self.assertEqual(States.CANCEL_SELL, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_transation_user_cancel_case_4(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

        testTradeObj.proceed(currentPrice=1)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.SELL_STANDBY, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.TRACE_SELL, testTradeObj.state)

        testTradeObj.stoploss()
        self.assertEqual(States.STOP_LOSS, testTradeObj.state)

        testTradeObj.proceed()
        self.assertEqual(States.ORDER_DONE, testTradeObj.state)

    def test_set_buyPrice(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        self.assertEqual(States.TRACE_BUY, testTradeObj.state)

    def test_condition_trasition_tracebuy_to_buydone(self):
        testTradeObj = tradeFactoryService.TradeState(
            mockRequests.MockRequests(), "KRW-BTC", 10, 1, 1, 1, 1, 1)
        testTradeObj.proceed(currentPrice=0)
        self.assertNotEqual(States.BUY_DONE, testTradeObj.state)

        testTradeObj.proceed(currentPrice=1)
        self.assertEqual(States.BUY_DONE, testTradeObj.state)
        self.assertEqual(testTradeObj.buyPrice, 1432)
        self.assertEqual(testTradeObj.quantity, 0.01)
