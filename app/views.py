from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm, LunchForm
import pymongo


@app.route('/')
@app.route('/index')
def index():
    user1= {'nickname': 'Arvind',
    		'statement': 'Fuck you Tahmid'} 
    user2= {'nickname': 'Tahmid',
    		'statement': 'But Whyyyyyyyyy'} # fake user
    return render_template('index.html',
                           title='Home',
                           user1=user1,
                           user2=user2)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = LoginForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			userInfo = db.userInfo
			print userInfo
			data = {}
			data['username'] = request.form['username']
			data['password'] = request.form['password']
			userInfo.insert(data)
			return redirect('/index')

		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return redirect('/index')
	else:
		return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			userInfo = db.userInfo
			usernameToVerify = list(userInfo.find({'username': request.form['username']}))
			if(len(usernameToVerify) == 0):
				return redirect('/login')
			elif(request.form['password'] == usernameToVerify[0]['password']):
				return redirect('www.google.com')
			else:
				return redirect('www.abc.xyz')


		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return redirect('/index')
	else:
		return render_template('login.html', title='Sign In', form=form)

@app.route('/addLunchRequest')
def showAddWish():
    return render_template('addWish.html')


@app.route('/lunchPost', methods=['GET', 'POST'])
def lunchPost():
	form = LunchForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			lunchDetails = db.lunchDetails
			data = {}
			data['title'] = request.form['title']
			data['post'] = request.form['post']
			lunchDetails.insert(data)
			return redirect('/index')
		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return redirect('/temp.html')
	else:
		return render_template('temp.html', title='ADD A WISH', form=form)


@app.route('/newsFeedStuff', methods=['GET', 'POST'])
def newsFeed():
	try:
		conn=pymongo.MongoClient()
		db = conn.pennapps
		lunchDetails = db.lunchDetails
		myList = list(lunchDetails.find())
		f = open('./templates/temporary.html','w')
		message = """<html>
		<head></head>
		<body><p> s""" + myList[0]['title'] + """</p></body>
		</html>"""
		f.write(message)

		f.close()
		return render_template('news.html')	
	except pymongo.errors.ConnectionFailure, e:
		print "Could not connect to MongoDB: %s" % e
		return redirect('/temp.html')



