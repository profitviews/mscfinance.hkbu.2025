from profitview import Link, http, logger
import sqlite3


class Trading(Link):
	ready = False
	store = False
	
    def on_start(self):
        self.con = sqlite3.connect(
			"trading.db", check_same_thread=False)
		logger.info("Created/connected sqlite db")
        self.init_trading_db()
		self.ready = True
        
    def init_trading_db(self):
        self.cur = self.con.cursor()
		self.cur.execute("DROP TABLE IF EXISTS trades")
        self.cur.execute("""
		CREATE TABLE 
		trades(src, sym, price, side, time)
		""")
	
    def trade_update(self, src, sym, data):
		if not self.ready or not self.store: return
	
		logger.info("Writing trade to DB")
        self.cur.execute("""
            INSERT INTO trades VALUES
            (?, ?, ?, ?, ?)
            """, 
			(src, sym, 
			 data['price'], data['side'], data['time']))
        self.con.commit()

    @http.route
    def post_start_storing(self, data):
		if not self.ready: return

		if data['start'].lower() == "true":
			logger.info("Start now")
			self.store = True
        return data	

	@http.route
    def post_count_of_trades(self, data):
		if not self.ready or not self.store: return 0
        trades_cur = self.con.cursor()
        trades_cur.execute("""
		SELECT count(*) from trades
		""")
        return trades_cur.fetchall()[0][0]

	@http.route
    def post_latest_trades(self, data):
		if not self.ready or not self.store: return
        trades_cur = self.con.cursor()
        trades_cur.execute("""
		SELECT * from trades order by time desc limit 10
		""")
        return trades_cur.fetchall()		

    @http.route
    def post_reset_trades(self, data):
		if not self.ready or not self.store: return
		logger.info("Removing stored trades from the database")
        self.con.cursor().execute("DROP TABLE IF EXISTS trades;")
        self.con.commit()
        self.init_trading_db()
