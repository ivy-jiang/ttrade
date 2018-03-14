#!/usr/bin/env python3

import sqlite3

connection=sqlite3.connect('master.db', check_same_thread=False)
cursor=connection.cursor()

cursor.execute(
	"""CREATE TABLE users(
	pk INTEGER PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(16),
	password VARCHAR(32)
	);"""

)


cursor.execute(
	"""CREATE TABLE positions(
	pk INTEGER PRIMARY KEY AUTOINCREMENT,
	userid INTEGER,
	ticker_symbol VARCHAR,
	number_of_shares INTEGER,
	volume_weighted_adjusted_price FLOAT,
	FOREIGN KEY (userid) REFERENCES users (pk)
	);"""
)


cursor.execute(
	"""CREATE TABLE transactions(
	pk INTEGER PRIMARY KEY AUTOINCREMENT,
	userid INTEGER,
	unix_time FLOAT,
	ticker VARCHAR,
	transaction_type BOOL,
	last_price FLOAT,
	trade_volume INTEGER,
	FOREIGN KEY (userid) REFERENCES users (pk)

	);"""
)





cursor.execute(
	"""CREATE TABLE bal_earn(
	pk INTEGER PRIMARY KEY AUTOINCREMENT,
	userid INTEGER,
	balance FLOAT,
	earnings FLOAT,
	FOREIGN KEY (userid) REFERENCES users (pk)
	);"""
	)



cursor.close()
connection.close()


