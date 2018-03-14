#!/usr/bin/env python3

from flask import Flask, flash, redirect, url_for, render_template, request
#from flask_login import login_required, current_user

from flask_bootstrap import Bootstrap
import time
import model
import pandas as pd

def captureid(idno1):
	return(int(idno1))

app =Flask(__name__)
Bootstrap(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
#app.secret_key = 'some_secret'


@app.route('/', methods=['GET'])
def home(message2=None):
	if request.referrer:
		return render_template('home.html',  message2= "You logged out. Wanna start again?")
	else:
		return render_template('home.html')
	# args = request.args.to_dict()
	# return_url = args.pop('return_url', None)
	# if return_url is None:
	# 	return render_template('home.html')
	# else:
	# 	return render_template('home.html',  message2= "hmm you logged out")


@app.route('/user/<message>', methods=['GET', 'POST'])
def user(message):
	if request.method=='GET':
		return render_template('user.html', message=message)
	else:
		#TODO if it is Post method
		useru=request.form['userexist']

		if useru in ['y', 'yes']:
			return redirect(url_for('askid'))
		elif useru in ['n', 'no']:
			return redirect(url_for('createid'))
			# idno=model.createuser()
			# idz1=captureid(idno)
			#
			# bal,earn=model.create(idz1)
			# mess="Successfully created new user."
			# return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idno, xbal=bal, xearn=earn))

		return render_template('user.html', message= "Bad input, either yes or no please.")



@app.route('/createid', methods=['GET', 'POST'])
def createid():
	if request.method=='GET':
		return render_template('createid.html')
	else:
		createn=request.form['createname']
		createpass=request.form['createpassword']
		createpass2=request.form['createpassword2']
		newobj=model.createcustomuser(createn,createpass, createpass2)

		if newobj == "Something wrong with ya input." or newobj == "Your password inputs do not match.":
			return render_template('createid.html', message='Bad input and stuff!')

		elif "Username already exists" in newobj:
			strreturn= 'Username already exists: '+ str(createn)
			return render_template('createid.html', message=strreturn)

		else:
			myid=newobj[3]
			myname=newobj[1]
			#mypass=newobj[3]
			idz1=captureid(myid)

			bal,earn=model.create(idz1)

			mess="Successful creation: "+str(myname)+"!  What next?"
			return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idz1, xbal=bal, xearn=earn))






@app.route('/askid', methods=['GET', 'POST'])
def askid():
	if request.method=='GET':
		return render_template('askid.html')
	else:
		#TODO if it is Post method
		idz=request.form['idask']
		passwordz=request.form['passwordz']
		###idz== we have the ID now.. refer to model?
		#idno=model.userauth(idz)
		idno=model.authcustomuser(idz,passwordz)
		# myid=idno[1]
		# myname=idno[2]
		# mypass=idno[3]

		if idno == "Bad inputz" or idno == "Bad ID & password input":
		 		return render_template('askid.html', message='Bad input and stuff!')
		else:
				myid=idno[1]
				myname=idno[2]
				mypass=idno[3]
				idz1=captureid(myid)

				bal,earn=model.create(idz1)

				mess="Successful input user id: "+str(myname)+"!  What next?"
				return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idz1, xbal=bal, xearn=earn))



@app.route('/landing/<message1>/<balance>/<earnings>/<idno>/<xbal>/<xearn>')
def landing(message1, balance, earnings, idno, xbal, xearn):
	#redirect(url_for("portfolio", idno=idno))
	idz1=idno

	return render_template('landing.html', message1=message1, balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn)



@app.route('/buy//<balance>/<earnings>/<idno>/<xbal>/<xearn>', methods=['GET', 'POST'])
def buy(balance, earnings, idno, xbal, xearn):
	if request.method=='GET':
		return render_template('buy.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn)
	else:
			# x= model.buy(ticker_symbol, trade_volume, bal, earn, idno)
			# return x
		tickersym=request.form['tickersymz']
		tradevolume=request.form['tradevol']
		bal,earn=model.create(idno)
		x= model.buy(tickersym, tradevolume, bal, earn, idno)
		zeez=x.split()
		if "Sorry," in zeez:
			message2="An error occured..."+x
			return render_template('buy.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn, message2=message2)
		else:
			mess="Successfully bought ticker and volume."+x
			idz1=captureid(idno)
			bal,earn=model.create(idz1)

			return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idno, xbal=bal, xearn=earn))



@app.route('/sell//<balance>/<earnings>/<idno>/<xbal>/<xearn>', methods=['GET', 'POST'])
def sell(balance, earnings, idno, xbal, xearn):
	if request.method=='GET':
		return render_template('sell.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn)
	else:
			# x= model.buy(ticker_symbol, trade_volume, bal, earn, idno)
			# return x
		tickersym=request.form['tickersymz']
		tradevolume=request.form['tradevol']
		bal,earn=model.create(idno)
		x= model.sell(tickersym, tradevolume, bal, earn, idno)
		zeez=x.split()
		if "Sorry," in zeez:
			message2="An error occured..."+x
			return render_template('sell.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn, message2=message2)
		else:
			mess="Successfully sold ticker and volume."+x
			idz1=captureid(idno)
			bal,earn=model.create(idz1)

			return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idno, xbal=bal, xearn=earn))




@app.route('/lookup/<balance>/<earnings>/<idno>/<xbal>/<xearn>', methods=['GET', 'POST'])
def lookup( balance, earnings, idno, xbal, xearn):
	if request.method=='GET':
		return render_template('lookup.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn)
	else:
		idz1=idno
		companyname=request.form['company1']
		x = model.lookup(companyname)
		zeez=x.split()
		if "Sorry," in zeez:
			message2="An error occured..."+x
			return render_template('lookup.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn, message2=message2)
		else:

			bal,earn=model.create(idz1)
			mess="your ticker is...."+x
			return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idno, xbal=bal, xearn=earn))



@app.route('/quote/<balance>/<earnings>/<idno>/<xbal>/<xearn>', methods=['GET', 'POST'])
def quote( balance, earnings, idno, xbal, xearn):
	if request.method=='GET':
		return render_template('quote.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn)
	else:
		idz1=idno
		quoting=request.form['quotez']
		x=model.quote(quoting)
		#zeez=x.split()
		if isinstance(x, str):
			message2="An error occured..."+x
			return render_template('quote.html', balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn, message2=message2)
		else:
			bal,earn=model.create(idz1)
			xstr=str(x)
			mess="the quote is "+xstr+" for {}.".format(quoting)
			return redirect(url_for("landing", message1=mess, balance=bal.balancez, earnings=earn.earningz, idno=idno, xbal=bal, xearn=earn))




@app.route('/portfolio/<balance>/<earnings>/<idno>/<xbal>/<xearn>', methods=['GET'])
def portfolio(balance, earnings, idno, xbal, xearn):
	idz1=idno
	bal,earn=model.create(idz1)
	name2="Your current portfolio holdings"
	z=model.retrieve(idno)
	if isinstance(z, str):
		return render_template('portfolio.html',balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn, data = z, name1=name2)
	else:
		return render_template('portfolio.html',balance=balance, earnings=earnings, idno=idno, xbal=xbal, xearn=xearn, data = z.to_html(), name1=name2)






# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	if request.method=='GET':
# 		return render_template('login.html')
# 	else:

# 		username=request.form['username']
# 		password=request.form['password']
#
# 		if username=='kenso':
# 			if password=='swordfish':
# 				pass
# 		return render_template('login.html', message= "bad credentials")
#
#
#


def user_all(idz2):

	print (game_loop(idz2))

###############################################
###############################################
###############################################

# def game_loop(idno):
#
# 	bal,earn=model.create(idno)
#
# 	putin= view.mainstuff(bal.balancez, earn.earningz, idno)
#
# 	user_input= view.main_menu()
# 	buy_inputs=['b','buy']
# 	sell_inputs=['s','sell']
# 	lookup_inputs=['l', 'lookup']
# 	quote_inputs=['q', 'quote']
# 	exit_inputs=['e', 'exit']
# 	portfolio_inputs=['p', 'portfolio']
#
#
# 	acceptable_inputs=buy_inputs \
# 			 + sell_inputs \
# 			 + lookup_inputs \
# 			 + quote_inputs \
# 			 +exit_inputs \
# 			+ portfolio_inputs
#
#
# 	on_off_switch= True
#
# 	while on_off_switch:
# 		if user_input.lower() in acceptable_inputs:
#
# 			if user_input.lower() in portfolio_inputs:
# 				z=model.retrieve(idno)
# 				return z
#
# 			elif user_input.lower() in buy_inputs:
# 				(ticker_symbol, trade_volume)= view.buy_menu()
# 				x= model.buy(ticker_symbol, trade_volume, bal, earn, idno)
# 				return x
#
#
# 			elif user_input.lower() in sell_inputs:
# 				(ticker_symbol, trade_volume)=view.sell_menu()
# 				x= model.sell(ticker_symbol, trade_volume, bal, earn, idno)
# 				return x
#
# 			elif user_input.lower() in lookup_inputs:
# 				company_name=view.lookup_menu()
# 				x = model.lookup(company_name)
# 				return x
#
# 			elif user_input.lower() in quote_inputs:
# 				ticker_symbol= view.quote_menu()
# 				x=model.quote(ticker_symbol)
# 				return x
#
# 			elif user_input.lower() in exit_inputs:
# 				return(">>> Sure you wanna leave???")
# 				break
# 				#on_off_switch= False
#
# 			else:
# 				print('bad input. restarting game in five seconds..')
# 				time.sleep(5)
# 				game_loop()
#
#
#
# 		else:
# 			print("Y R U A nub? deadz, please run it again.")
# 			break


# def user_all():
# 	#yaresponse is USERID ok.. so very useful to ID user
# 	yaresponse= userman()
# 	if yaresponse == 'bad':
# 		print ("No no, please run program again with correct stoof.")
# 		return()
#
#
# 	elif yaresponse == 'by':
# 		print("  Will miss ya (^.^) ")
# 	else:
# 		print(game_loop(yaresponse))
#
# 		while True:
# 			geez= view.cont()
#
# 			if geez.lower() in ['c','continue']:
# 				print (game_loop(yaresponse))
# 			else:
# 				print("Cyaz")
# 				break
#


# def userman():
# 	meowuser= view.askuser() ##login.html
# 	if meowuser.lower() in ['y', 'yes']:
# 		getid= view.userreq()
# 		idno=model.userauth(getid)
# 		if idno == "Bad ID input":
# 			return("bad")
# 		else:
# 			view.tellid(idno)
# 			return(idno)
# 	elif meowuser.lower() in ['n', 'no']:
# 		idno=model.createuser()
# 		view.tellid(idno)
# 		return(idno)
#
# 	else:
# 		print ("  Bye byez!!")
# 		return("by")

# def loo():
# 	ya= True
# 	while True:
# 		geez= view.cont()
#
# 		if geez.lower() in ['c','continue']:
# 			print (game_loop())
# 		else:
# 			print("Cyaz")
# 			break

if __name__=='__main__':
#	from pprint import pprint
#	print(game_loop())
#	loo()
#	print (user_all())
	#settings for local environment
	app.run(host='127.0.0.1', port=4000, debug=True)
#	app.run(debug=True)
#	user_all()
