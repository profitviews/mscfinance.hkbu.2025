from profitview import Link, logger
import talib
import numpy as np 


class Trading(Link):
	ready = False
	
    VENUE = 'WooPaper'
    REVERSION = .1
    LOOKBACK = 5
    SIZE = 0.0001  # BTC 

	def on_start(self):
        self.prices = np.array([], dtype=float)
		self.elements = 0
		self.mean = 0
		logger.info(f"{self.VENUE} {self.REVERSION} {self.LOOKBACK} {self.SIZE}")
		self.ready = True

    def trade_update(self, src, sym, data):
		if not self.ready: return
	
		newPrice = float(data["price"])
        self.prices = np.append(self.prices, newPrice)
		logger.info(f"{src} {sym} {newPrice=}")
        if len(self.prices) <= self.LOOKBACK:
            # Until we have enough data for the mean
            self.mean = np.mean(self.prices)
        else:  # Move and recalculate mean
            self.prices = self.prices[1:]
            self.mean = np.mean(self.prices)
			stddev = talib.STDDEV(self.prices, timeperiod=self.LOOKBACK)[-1] 
			logger.info(f"\n{stddev=}\n")
            stdReversion = self.REVERSION*stddev
			logger.info(f"checking for extreme")
            if newPrice > self.mean + stdReversion:  # Upper extreme - Sell!
				logger.info("Time to sell")
                self.create_market_order(self.VENUE, sym, "Sell", self.SIZE)
            if newPrice < self.mean - stdReversion:  # Lower extreme - Buy!
				logger.info("Time to buy")
                self.create_market_order(self.VENUE, sym, "Buy", self.SIZE)