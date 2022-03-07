import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from project.models.init_db import db


class TradeStateModel(db.Model):
    """Trade model"""
    __tablename__ = 'tradeStateDatas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    trade_state = Column(Integer, nullable=False)
    ticker = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    predictBuyPrice = Column(Integer, nullable=False)
    predictSellPrice = Column(Integer, nullable=False)
    trailingStopPercent = Column(Float, nullable=False)
    trailingTriggerPercent = Column(Float, nullable=False)
    stoplossPercent = Column(Float, nullable=False)
    buyPrice = Column(Integer, nullable=False)
    sellPrice = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)

    def __init__(self, uuid, ticker, balance, predictBuyPrice, predictSellPrice, trailingStopPercent, trailingTriggerPercent, stoplossPercent):
        self.uuid = uuid
        self.predictBuyPrice = predictBuyPrice
        self.predictSellPrice = predictSellPrice
        self.trailingStopPercent = trailingStopPercent
        self.trailingTriggerPercent = trailingTriggerPercent
        self.trailingStopPercent = trailingStopPercent
        self.stoplossPercent = stoplossPercent
        self.balance = balance
        self.ticker = ticker

class OrderIdModel(db.Model):
    """OrderIdModel"""
    __tablename__ = 'orderIds'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, nullable=False)
    orderId = Column(String, nullable=False)
    orderType = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)