# encoding: utf-8
from flask import jsonify, request
from flask_script import Manager
from flask_cors import CORS, cross_origin
import json

from project.app import create_app
from project.services import tradeFactoryService

tradeSvc = tradeFactoryService.TradeFactoryService();
app = create_app()
CORS(app, resources={r'*': {'origins': '*'}})

manager = Manager(app)

@app.route("/dotrade", method=['POST'])
def dotrade():
    
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return {'status': 'not enough parameter'}

    


    return jsonify(market.get_ohlcv(ticker, priod))

if __name__ == '__main__':
    manager.run()
