from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import datetime  # For datetime objects
from DataFeeds.MyJSONFeed import MyJSONFeed
import os
import sys
from data import json_data
import pandas as pd
from backtrader import TimeFrame


class OptimizerCerebro(bt.Cerebro):
    options = {
        "fromdate": datetime.datetime(2010, 3, 1, 19, 0, 0),
        "todate": datetime.datetime(2020, 3, 1, 20, 0, 0),
        "endvalue": 0,
        "symbol": 'EUR_USD',
        "timeframe": bt.TimeFrame.Days,
        "compression": 1
    }

    def __init__(self, options):
        super().__init__()
        self.options.update(options)

    @property
    def run(self):
        # Create a cerebro entity
        cerebro = bt.Cerebro()
        startcash = 100000

        # Add a strategy
        if "strategy" not in self.options:
            return False

        cerebro.optstrategy(self.options["strategy"], period=range(14, 21))
        # json_data = to_json()

        opens = []
        closes = []
        highs = []
        lows = []
        volumes = []
        times = []
        for i in range(len(json_data)):
            times.append(json_data[i]["time"])
            opens.append(json_data[i]["open"])
            highs.append(json_data[i]["high"])
            lows.append(json_data[i]["low"])
            closes.append(json_data[i]["close"])
            volumes.append(json_data[i]["volume"])

        df = pd.DataFrame(zip(times, opens, highs, lows, closes, volumes), columns=['datetime','open','high','low','close','volume'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        # print(df)
        data = MyJSONFeed(dataname=df)

        # Add the data to Cerebro
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(startcash)
        cerebro.run()

    def to_json():

        server = "http://urlToAPI.json"
        timeframe = 'D'
        granularity = self.options["timeframe"]
        if self.options["timeframe"] == TimeFrame.Minutes:
            timeframe = 'M'
            granularity = self.options["timeframe"] + str(self.options["compression"])

        postParameter = {
            'data[instrument]': self.options["symbol"],
            'data[granularity]': granularity,
            'data[from]': datetime.datetime.strptime(self.options["fromdate"]),
            'data[to]': datetime.datetime.strptime(self.options["fromdate"]),
        }
        payload = urllib.parse.urlencode(postParameter)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", server, headers=headers, data=payload)
        result = json.loads(response.text.encode('utf8'))

        return result