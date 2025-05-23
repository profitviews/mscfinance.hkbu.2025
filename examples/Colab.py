from profitview import Link, http, logger

# This is a ProfitView script showing how to control a Bot via a webhook.  
# It should be copied to the ProfitView Signals interface and run from there.
# For example it can be triggered from a GoogleColab notebook.

class Trading(Link):
	ready = False
	start = False

    def on_start(self):
		self.ready = True
		logger.info("Ready")

    def trade_update(self, src, sym, data):
		if self.ready and self.start:
			logger.info(f"Traded {sym} at {data['price']}")

    @http.route
    def get_route(self, data):
        """Definition of GET request endpoint - see docs for more info"""
        return data

    @http.route
    def post_start(self, data):
		if data['start'].lower() == "true":
			logger.info("Start now")
			self.start = True
        return data
