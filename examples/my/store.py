import sqlite3


class Store:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(
            db_name, check_same_thread=False)

    def init_db(self, table_name):
        self.cur = self.con.cursor()
        self.table_name = table_name
        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cur.execute(f"""
            CREATE TABLE
            {table_name}(src, sym, price, side, time)
            """)

    def write_trades(self, src, sym, data):
        self.cur.execute(f"""
        INSERT INTO {self.table_name} VALUES
        (?, ?, ?, ?, ?)
        """,
                     (src, sym,
                     data['price'], data['side'], data['time']))
        self.con.commit()

    def trade_count(self):
        trades_cur = self.con.cursor()
        trades_cur.execute("""
            SELECT count(*) from trades
            """)
        return trades_cur.fetchall()[0][0]

    def latest_trades(self, number):
        trades_cur = self.con.cursor()
        trades_cur.execute(f"""
            SELECT * from trades order by time desc limit {number}
            """)
        return trades_cur.fetchall()

    def reset_trades(self):
        self.con.cursor().execute(f"""
        DROP TABLE IF EXISTS {self.table_name}""")
        self.con.commit()
        self.init_db(self.table_name)
