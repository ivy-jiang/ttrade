#!/usr/bin/env python3
import json
import requests
import sqlite3
import time
import pandas as pd

##not case sensitive..
def createcustomuser(name, password, passx):
	try:
		name=str(name)
		name1=name.lower()
		password=str(password)
		password1=password.lower()
		passx=str(passx)
		password2=passx.lower()
		if password2 == password1:
			connection=sqlite3.connect('master.db', check_same_thread=False)
			cursor=connection.cursor()
			cursor.execute("""SELECT * from users where username='{}';""".format(name1))
			cap=cursor.fetchone()
			connection.commit()
			# creating new user:
			if cap==None:
				cursor.execute("INSERT INTO users(username, password) VALUES('{}', '{}');".format(name1, password1))
				connection.commit()
				cursor.execute("SELECT pk from users ORDER BY pk DESC;")
				newnew=cursor.fetchone()
				usid=int(newnew[0])
				cursor.close()
				connection.close()
				return(("Success creation.. Username: ", name1, "User ID: ", usid))
			# Username already exists
			else:
				cursor.close()
				connection.close()
				return(("Username already exists: ", name1))
		else:
			return("Your password inputs do not match.")
	except:
		return("Something wrong with ya input.")

def authcustomuser(name, password):
	try:
		name=str(name)
		password=str(password)
		connection=sqlite3.connect('master.db', check_same_thread=False)
		cursor=connection.cursor()
		cursor.execute("SELECT * from users where username='{}' and password= '{}';".format(name, password))
		getii=cursor.fetchone()
		propname=str(getii[1])
		proppass=str(getii[2])
		propid=int(getii[0])
		cursor.close()
		connection.close()
		if getii == None:
			return ("Bad inputz")
		else:
			return (("Successful login", propid, propname, proppass))

	except:
		return ("Bad ID & password input")
#######################################################
#######################################################

def createuser():
	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()
	cursor.execute("INSERT INTO users(username, password) VALUES('{}', '{}');".format("nub", "let"))
	connection.commit()
	cursor.execute("SELECT pk from users ORDER BY pk DESC;")
	newnew=cursor.fetchone()
	myid=store_id(int(newnew[0]))
	return( int(newnew[0]))


def userauth(idinput):
	try:
		idinput=int(idinput)
		connection=sqlite3.connect('master.db', check_same_thread=False)
		cursor=connection.cursor()
		cursor.execute("SELECT * from users where pk= {};".format(idinput))
		getii=cursor.fetchone()
		myid=store_id(int(getii[0]))
		return( int(getii[0]))

	except:
		return ("Bad ID input")
#myid.idz
class store_id():
	def __init__(self, idno):
		self.idz=idno

def create(idno):
	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()
	cursor.execute("SELECT * from bal_earn where userid={} ORDER BY pk DESC;".format(idno))
	capture1=cursor.fetchone()
	if capture1 == None:
		xbal=Balance(1000) #1000 is default balance
		xearn=Earnings(0) #0 default earnings
		cursor.execute("""INSERT INTO bal_earn(userid, balance, earnings)
			 VALUES(?, ?, ?);""", (idno, 1000,0))
		connection.commit()

	else:
		xbal=Balance(capture1[2])
		xearn=Earnings(capture1[3])
	connection.commit()
	cursor.close()
	connection.close()
	return (xbal, xearn)
	#xbal is balance object, xearn is earnings object.. so get_func for value



class Balance():
	#update everytime successfully buy / sell
	def __init__(self, input2):
		self.balancez=input2

	def get_balance(self):
		print (self.balancez)

	def set_balance(self, bal):
		self.balancez=bal

class Earnings():
	def __init__(self, earning):
		self.earningz=earning
	def get_earnings(self):
		return (self.earningz)
	def set_earnings(self, earn):
		self.earningz=earn

def adj_balance_earnings( price, vol, transac_cost, type, ticker, xbal, xearn, idno):
	##earnings=(soldvol *sold price) - (soldvol *vwap)
	vol=float(vol)
	price=float(price)
	transac_cost=float(transac_cost)
	if type == 1: #buying so reduce balance
		calc= ( vol* price) + transac_cost
		adj=xbal.balancez-calc
		xbal.set_balance(adj)

		calcz=xearn.earningz- transac_cost
		xearn.set_earnings(calcz)
		bal3=adj
		earn3=calcz

	else: ##selling, reduce balance + increase (hopefully) earnings
		calc= (vol* price) - transac_cost
		adj=xbal.balancez+calc
		xbal.set_balance(adj)

		rev=float(price*vol)
		vwap3=float(vwap(ticker, idno))
		cost=float(vol*vwap3)
		##earnings for the ticker is( sold vol * sold price) -( sold vol * vwap)
		earnTicker=rev-cost
#		print (rev, cost, vwap3,xearn.earningz, earnTicker)
		#modifying me earnings:
		adding=	xearn.earningz+earnTicker-transac_cost
		xearn.set_earnings(adding)
		bal3=adj
		earn3=adding

	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()
	cursor.execute(" INSERT INTO bal_earn(userid, balance, earnings) VALUES({}, {}, {});".format(idno, bal3, earn3))
	connection.commit()
	cursor.close()
	connection.close()
#	print ('finally check',bal3, xbal.balancez,earn3, xearn.earningz)

	return( "Balance: ", xbal.balancez, "Earnings: ", xearn.earningz )



def buy(ticker_symbol, trade_volume, xbal, xearn,idno):
	ticker_symbol=ticker_symbol.upper()

	try:
		deep_link= 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
		response=json.loads(requests.get(deep_link).text)
		last_price=response['LastPrice']

		friction= 8.00 #amount of money it costs to make a trade per trade /broker fee
		transaction_cost= (int( trade_volume) *float(last_price)) + friction #algorithm!!!

		if transaction_cost > xbal.balancez:
			return "Sorry, Not enuf money !"
		#prnt error message/ return an error msg to controller
		else:
			nowtime=time.time()
			cc= write_transactions(nowtime, ticker_symbol, 1, last_price, trade_volume, idno)
			##adj balance and earnings:
			b_e= adj_balance_earnings(last_price, trade_volume, friction, 1, ticker_symbol, xbal, xearn, idno)
			#should return transac message and new balance& earnings

			printy=["Great! ",str( cc), str(b_e)]
			zprin= " ".join(printy)
			return(zprin)
#			return("Ok!", cc, b_e)

	except KeyError:
#		print("Oh noes, no understand wat u enter mate D: ")
#		return()
		return("Sorry, error! Not understand wat u enter")

def sell(ticker_symbol, trade_volume, xbal, xearn, idno):

	try:
		ticker_symbol=ticker_symbol.upper()
		deep_link= 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
		response=json.loads(requests.get(deep_link).text)
		last_price=response['LastPrice']

		connection=sqlite3.connect('master.db', check_same_thread=False)
		cursor=connection.cursor()

		friction= 8.00 #amount of money it costs to make a trade per trade /broker fee
	#check db if have ticker and q
		cursor.execute("""SELECT * from positions where ticker_symbol='{}' and userid={};""".format(ticker_symbol, idno))
		cap=cursor.fetchone()
		connection.commit()

		cursor.close()
		connection.close()

		try:
			 int(trade_volume)
		except:
			return ("Sorry, does not work.")
		if cap is None or cap[3]<int(trade_volume):

			return("Sorry, you do not have the stock and/or quantity...hmm")

		else:
			if friction < xbal.balancez:
				nowtime=time.time()

				cc= write_transactions(nowtime, ticker_symbol, 0, last_price, trade_volume, idno)

			#update balance & earnings
				b_e= adj_balance_earnings(last_price, trade_volume, friction, 0, ticker_symbol, xbal, xearn, idno)

			#should return transac message and new balance
				printy=["Great! ",str( cc), str(b_e)]
				zprin= " ".join(printy)
				return(zprin)

			else:
#				print("Yo you do not have enough balance to cover friction. ")
#				return()
				return("Sorry, not enough balance to cover friction")


	except KeyError:

#		print("No!! What an error. Plz try again! ")
#		return()
		return("No! Sorry, doesn't work.")


def write_transactions(time, ticker, type, price, volume, idno):
	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()

	ticker=ticker.upper()
	cursor.execute("""INSERT INTO transactions(userid, unix_time, ticker, transaction_type, last_price, trade_volume) VALUES ({}, {},"{}", {}, {}, {});""".format(idno, time, ticker, type, price, volume))
	connection.commit()

	##update write_positions i.e. positions table
	zz= write_positions(ticker, volume, type, idno)

	cursor.close()
	connection.close()
	return("Written your action to transactions database! ")


def write_positions(ticker_symbol, number_of_shares, type, idno):

	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()
	ticker_symbol=ticker_symbol.upper()
	#caling vwap here
	vwap2=vwap(ticker_symbol, idno)

	cursor.execute("""SELECT * FROM positions where ticker_symbol="{}" and userid={}; """.format(ticker_symbol, idno))
	captureTicker= cursor.fetchone()
	if captureTicker == None:
		##buying and not exist yet so INSERT!!!
		cursor.execute("""INSERT INTO positions(userid, ticker_symbol, number_of_shares,
		volume_weighted_adjusted_price) VALUES({},"{}",{},{})""".format(idno, ticker_symbol, number_of_shares, vwap2))

		connection.commit()

	else:	##update values... NOT INSERT BUT UPDATE!!!

		cursor.execute("""SELECT number_of_shares,
		volume_weighted_adjusted_price
		FROM positions where ticker_symbol="{}" and userid= {};""".format(ticker_symbol, idno))

		vol_vwap= cursor.fetchone()
		connection.commit()

		if type == 0: #if selling.. reduce position i.e. minus volume

			newvol=vol_vwap[0]-int(number_of_shares)

			if newvol==0:
				cursor.execute("""DELETE from positions WHERE ticker_symbol="{}" and userid={}; """.format(ticker_symbol, idno))
				connection.commit()

			else:
				cursor.execute("""UPDATE positions SET number_of_shares= {},
					volume_weighted_adjusted_price ={} where ticker_symbol="{}" and userid={};""".format( newvol, vwap2, ticker_symbol, idno))
				connection.commit()

		else: ##buying so add volume
			newvol=vol_vwap[0]+ int(number_of_shares)
			cursor.execute("""UPDATE positions SET number_of_shares = {},
			volume_weighted_adjusted_price={} where ticker_symbol="{}" and userid={}; """.format( newvol, vwap2, ticker_symbol, idno))
			connection.commit()

	connection.commit()
	cursor.close()
	connection.close()
	return("Updated positions table!  ")


def vwap(ticker, idno):
	ticker=ticker.upper()
	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()

	cursor.execute("""SELECT * FROM transactions where ticker="{}" and userid={}; """.format(ticker, idno))
	captureTicker= cursor.fetchall()
	if captureTicker==[]:
		pass
	else:

		cursor.execute("""SELECT last_price from transactions where ticker='{}' and userid={} and transaction_type=1;""".format(ticker, idno))
		pricex= cursor.fetchall()
		priceL= [price[0] for price in pricex]


		cursor.execute("""SELECT trade_volume from transactions where ticker='{}' and userid={} and transaction_type=1;""".format(ticker, idno))
		volx=cursor.fetchall()
		volL=[vol[0] for vol in volx]


		prod1=[vol*price for vol, price in zip(volL, priceL)]
		vwapz=sum(prod1)/sum(volL)


	connection.commit()
	cursor.close()
	connection.close()
	##sum(volume bought*price)/sum(volume bought)
	print ("Updated VWAP for {}".format(ticker))
	return(vwapz)




def lookup(company_name):

	try:
		deep_link= 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input={company_name}'.format(company_name=company_name)
		response=json.loads(requests.get(deep_link).text)
		ticker_symbol= response[0]['Symbol']
	#	print (ticker_symbol)
		return ticker_symbol

	except:

		print("Not good input MAN!!!!!")
		return("Sorry, You can try againz")
#		return ("No no!!!! Not good input!! ")

#curl the deep link to see


def quote(ticker_symbol):

	try:
		deep_link= 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
		response=json.loads(requests.get(deep_link).text)
		last_price=response['LastPrice']
	#	print (last_price)
		return last_price
	except:

		print("Not gud input DUDE!!!!")
		return("Sorry, you can try again.")
#		return ("No no!!!! Not good input")

def retrieve(idno):
	connection=sqlite3.connect('master.db', check_same_thread=False)
	cursor=connection.cursor()

	if len(pd.read_sql_query("SELECT * from positions where userid={};".format(idno), connection))== 0:
		xtable="No positions"
		return ("...well you have no positions.")

	else:

		xtable= (pd.read_sql_query("SELECT userid, ticker_symbol, number_of_shares, volume_weighted_adjusted_price from positions where userid={};".format(idno), connection))
		#print (xtable)
		#print (pd.read_sql_query("SELECT userid, ticker_symbol, number_of_shares, volume_weighted_adjusted_price from positions where userid={};".format(idno), connection))

	connection.commit()
	cursor.close()
	connection.close()
	return (xtable)




	# else:
	#
	# 	print (pd.read_sql_query("SELECT userid, ticker_symbol, number_of_shares, volume_weighted_adjusted_price from positions where userid={};".format(idno), connection))
	#
	# connection.commit()
	# cursor.close()
	# connection.close()
	# return()


if __name__ == "__main__":
	##kind of testing area
	from pprint import pprint
#	create()
#	print (buy('tsla', 1))
#	pprint (quote (lookup('Tesla')))
#	print(vwap('TSLA'))
#	print (retrieve(1))
#	print (createcustomuser("meowman", "pass2", "pass2"))
	print (authcustomuser("meowman", "pass2"))
