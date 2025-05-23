from profitview import Link, http, logger
from my.store import Store


class Trading(Link):
	ready = False
	
    def on_start(self):
		self.store = Store("trading.db")
		self.store.init_db("trades")
		self.ready = True
		logger.info("Ready")
        
    def trade_update(self, src, sym, data):
		if not self.ready: return
		self.store.write_trades(src, sym, data)
	
    @http.route
    def post_count_of_trades(self, data):
		if not self.ready: return 0
	
		return self.store.trade_count()

	@http.route
    def post_latest_trades(self, data):
		if not self.ready: return 0
	
        return self.store.latest_trades(10)

    @http.route
    def post_reset_trades(self, data):
		if not self.ready: return
	
		self.store.reset_trades()
