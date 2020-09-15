import datetime  # For datetime objects
import backtrader as bt

from Cerebros.OptimizerCerebro import OptimizerCerebro
from Strategies.RSIBorderBounce import RSIBorderBounce

if __name__ == '__main__':
    testStrategy = OptimizerCerebro({
        "strategy": RSIBorderBounce,
        "fromdate": datetime.datetime(2015, 1, 1),
        "todate": datetime.datetime(2015, 3, 1),
        "endvalue": 0,
        "symbol": 'XAG_USD',
        "timeframe": bt.TimeFrame.Days,
        "compression": 1
    })
    testStrategy.run