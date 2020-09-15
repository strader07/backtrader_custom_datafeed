import backtrader as bt


class RSIBorderBounce(bt.Strategy):
    params = (
        ('period', 21),
    )

    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.dataclose = self.datas[0].close
        self.rsi = bt.indicators.RSI_SMA(self.dataclose, period=self.params.period, safediv=True)

    def next(self):
        if self.position:
            print(self.position)
        if not self.position:

            if self.rsi < 30:
                self.log('buy, %.2f' % self.dataclose[0])
                self.buy(size=1)
        else:
            if self.rsi > 70:
                self.log('sell, %.2f' % self.dataclose[0])
                self.sell(size=1)

    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash, 2)
        print('RSI Period: {} Final PnL: {}'.format(
            self.params.period, pnl))