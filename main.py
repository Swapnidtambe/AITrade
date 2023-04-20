from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import date

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']



            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_accounts VALUES (NULL, %s, %s, %s,NULL,NULL)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/script')
def script():
    if 'loggedin' in session:
        return render_template('script_names.html')
    else:
        return redirect(url_for('login'))

@app.route('/pythonlogin/script/xauusd')
def xauusd():
    if 'loggedin' in session:
        today = date.today()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE id = %s', (session['id'],))
        # Fetch one record and r*eturn result
        end_date = cursor.fetchone()
        end_date = end_date['end_date']

        if end_date is None or end_date < today:
            return "not subscribed"

        else:
            return render_template('xauusd.html')
    else:
        return redirect(url_for('login'))

@app.route('/pythonlogin/script/eurusd')
def eurusd():
    if 'loggedin' in session:
        today = date.today()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE id = %s', (session['id'],))
        # Fetch one record and r*eturn result
        end_date = cursor.fetchone()
        end_date = end_date['end_date']

        if end_date is None or end_date < today:
            return "not subscribed"

        else:
            return render_template('eurusd.html')
    else:
        return redirect(url_for('login'))

@app.route('/pythonlogin/script/oil')
def oil():
    if 'loggedin' in session:
        today = date.today()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE id = %s', (session['id'],))
        # Fetch one record and r*eturn result
        end_date = cursor.fetchone()
        end_date = end_date['end_date']

        if end_date is None or end_date < today:
            return "not subscribed"

        else:
            return render_template('oil.html')
    else:
        return redirect(url_for('login'))

@app.route('/pythonlogin/subscription')
def subscription():
    if 'loggedin' in session:
        return render_template('subscription.html',subscription = session["subscription"])
    else:
        return redirect(url_for('login'))

@app.route('/pythonlogin/buysubscription')
def buysubscription():
    if 'loggedin' in session:
        return render_template('buysubscription.html')
    else:
        return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)



