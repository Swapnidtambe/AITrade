from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from app_property import AppProperty
import jwt
import datetime
from datetime import date


from config import Config
app_property = AppProperty()
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'my_secret_key'  # Replace with your own secret key
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)  # Set token expiration time

# Intialize MySQL
mysql = MySQL(app)

# In-memory store for blacklisted tokens (i.e. tokens that have been logged out)
blacklist = set()

# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/ai_trade/login/', methods=['POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    response = {}
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        data = request.get_json()
        username = data['username']
        password = data['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            payload = {'username': username, 'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            response['data'] = {'token': token}
            response['errorCode'] = ''
            response['errorMessage'] = ''
            response['status'] = 'OK'
            # Redirect to home page
            return response
        else:
            # Account doesnt exist or username/password incorrect
            msg = app_property.get_message('101')
            response['data'] = account
            response['errorCode'] = '101'
            response['errorMessage'] = msg
            response['status'] = 'FAIL'
            # Show the login form with message (if any)
        return response


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/ai_trade/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data['token']

    blacklist.add(token)
    return jsonify({'message': 'Token has been logged out'})



@app.route('/ai_trade/register', methods=['POST'])
def register():
    response = {}
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        data = request.get_json()
        # Create variables for easy access
        username = data['username']
        password = data['password']
        email = data['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            response['data'] = ''
            response['errorMessage'] = app_property.get_message('102')
            response['errorCode'] = '102'
            response['status'] = 'FAIL'
            return response

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            response['data'] = ''
            response['errorMessage'] = app_property.get_message('103')
            response['errorCode'] = '103'
            response['status'] = 'FAIL'
            return response

        elif not re.match(r'[A-Za-z0-9]+', username):
            response['data'] = ''
            response['errorMessage'] = app_property.get_message('104')
            response['errorCode'] = '104'
            response['status'] = 'FAIL'
            return response

        elif not username or not password or not email:
            response['data'] = ''
            response['errorMessage'] = app_property.get_message('105')
            response['errorCode'] = '105'
            response['status'] = 'FAIL'
            return response

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_accounts VALUES (NULL, %s, %s, %s,NULL,NULL)', (username, password, email,))
            mysql.connection.commit()
            response['data'] = 'You have successfully registered!'
            response['errorMessage'] = ''
            response['errorCode'] = ''
            response['status'] = 'OK'
            return response




# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/ai_trade/home/ai_summury', methods=['GET'])
def ai_summury():
    response = {}
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response["data"] = ''
        response['errorMessage'] = 'Authorization header is missing'
        response['errorCode'] = '107'
        response['status'] = 'FAIL'
        return response
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        response["data"] = ''
        response['errorMessage'] = 'Invalid token format'
        response['errorCode'] = '108'
        response['status'] = 'FAIL'
        return response
    token = parts[1]
    if token in blacklist:
        response["data"] = ''
        response['errorMessage'] = 'Token has been logged out'
        response['errorCode'] = '109'
        response['status'] = 'FAIL'
        return response
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        response['data'] = 'this is summary of forex market news'
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        response['data'] = ''
        response['errorMessage'] = 'Token has expired'
        response['errorCode'] = '110'
        response['status'] = 'FAIL'
        return response
    except jwt.InvalidTokenError:
        response['data'] = ''
        response['errorMessage'] = 'Invalid token'
        response['errorCode'] = '111'
        response['status'] = 'FAIL'
        return response


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/ai_trade/profile', methods=['GET'])
def profile():
    response = {}
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response["data"] = ''
        response['errorMessage'] = 'Authorization header is missing'
        response['errorCode'] = '107'
        response['status'] = 'FAIL'
        return response
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        response["data"] = ''
        response['errorMessage'] = 'Invalid token format'
        response['errorCode'] = '108'
        response['status'] = 'FAIL'
        return response
    token = parts[1]
    if token in blacklist:
        response["data"] = ''
        response['errorMessage'] = 'Token has been logged out'
        response['errorCode'] = '109'
        response['status'] = 'FAIL'
        return response
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        username = payload['username']
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        response['data'] = account
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        response['data'] = ''
        response['errorMessage'] = 'Token has expired'
        response['errorCode'] = '110'
        response['status'] = 'FAIL'
        return response
    except jwt.InvalidTokenError:
        response['data'] = ''
        response['errorMessage'] = 'Invalid token'
        response['errorCode'] = '111'
        response['status'] = 'FAIL'
        return response


@app.route('/ai_trade/script')
def script():
    response = {}
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response["data"] = ''
        response['errorMessage'] = 'Authorization header is missing'
        response['errorCode'] = '107'
        response['status'] = 'FAIL'
        return response
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        response["data"] = ''
        response['errorMessage'] = 'Invalid token format'
        response['errorCode'] = '108'
        response['status'] = 'FAIL'
        return response
    token = parts[1]
    if token in blacklist:
        response["data"] = ''
        response['errorMessage'] = 'Token has been logged out'
        response['errorCode'] = '109'
        response['status'] = 'FAIL'
        return response
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        msg = "Please select the following script: GOLD, EURO, JPY"
        response['data'] = msg
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        response['data'] = ''
        response['errorMessage'] = 'Token has expired'
        response['errorCode'] = '110'
        response['status'] = 'FAIL'
        return response
    except jwt.InvalidTokenError:
        response['data'] = ''
        response['errorMessage'] = 'Invalid token'
        response['errorCode'] = '111'
        response['status'] = 'FAIL'
        return response

@app.route('/ai_trade/script/gold')
def xauusd():
    response = {}
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response["data"] = ''
        response['errorMessage'] = 'Authorization header is missing'
        response['errorCode'] = '107'
        response['status'] = 'FAIL'
        return response
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        response["data"] = ''
        response['errorMessage'] = 'Invalid token format'
        response['errorCode'] = '108'
        response['status'] = 'FAIL'
        return response
    token = parts[1]
    if token in blacklist:
        response["data"] = ''
        response['errorMessage'] = 'Token has been logged out'
        response['errorCode'] = '109'
        response['status'] = 'FAIL'
        return response
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        msg = "This is the XAUUSD Signal"
        response['data'] = msg
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        response['data'] = ''
        response['errorMessage'] = 'Token has expired'
        response['errorCode'] = '110'
        response['status'] = 'FAIL'
        return response
    except jwt.InvalidTokenError:
        response['data'] = ''
        response['errorMessage'] = 'Invalid token'
        response['errorCode'] = '111'
        response['status'] = 'FAIL'
        return response

@app.route('/ai_trade/script/euro')
def eurusd():
    response = {}
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response["data"] = ''
        response['errorMessage'] = 'Authorization header is missing'
        response['errorCode'] = '107'
        response['status'] = 'FAIL'
        return response
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        response["data"] = ''
        response['errorMessage'] = 'Invalid token format'
        response['errorCode'] = '108'
        response['status'] = 'FAIL'
        return response
    token = parts[1]
    if token in blacklist:
        response["data"] = ''
        response['errorMessage'] = 'Token has been logged out'
        response['errorCode'] = '109'
        response['status'] = 'FAIL'
        return response
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        msg = "This is the EUR/USD Signal"
        response['data'] = msg
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        response['data'] = ''
        response['errorMessage'] = 'Token has expired'
        response['errorCode'] = '110'
        response['status'] = 'FAIL'
        return response
    except jwt.InvalidTokenError:
        response['data'] = ''
        response['errorMessage'] = 'Invalid token'
        response['errorCode'] = '111'
        response['status'] = 'FAIL'
        return response

@app.route('/ai_trade/script/jpy')
def USDJPY():
    response = {}
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        response["data"] = ''
        response['errorMessage'] = 'Authorization header is missing'
        response['errorCode'] = '107'
        response['status'] = 'FAIL'
        return response
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        response["data"] = ''
        response['errorMessage'] = 'Invalid token format'
        response['errorCode'] = '108'
        response['status'] = 'FAIL'
        return response
    token = parts[1]
    if token in blacklist:
        response["data"] = ''
        response['errorMessage'] = 'Token has been logged out'
        response['errorCode'] = '109'
        response['status'] = 'FAIL'
        return response
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        msg = "This is the USD/JPY Signal"
        response['data'] = msg
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        response['data'] = ''
        response['errorMessage'] = 'Token has expired'
        response['errorCode'] = '110'
        response['status'] = 'FAIL'
        return response
    except jwt.InvalidTokenError:
        response['data'] = ''
        response['errorMessage'] = 'Invalid token'
        response['errorCode'] = '111'
        response['status'] = 'FAIL'
        return response

@app.route('/ai-trade/subscription')
def subscription():
    if 'loggedin' in session:
        return render_template('subscription.html',subscription = session['end_date'])
    else:
        return redirect(url_for('login'))

@app.route('/ai-trade/buysubscription')
def buysubscription():
    if 'loggedin' in session:
        return render_template('buysubscription.html')
    else:
        return redirect(url_for('login'))

@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authorization header is missing'}), 401
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        return jsonify({'message': 'Invalid token format'}), 401
    token = parts[1]
    if token in blacklist:
        return jsonify({'message': 'Token has been logged out'}), 401
    try:
        payload = jwt.decode(token,'my_secret_key',algorithms='HS256')

        # user_id = payload['id']
        username = payload['username']
        return username
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401





if __name__ == "__main__":
    app.run(debug=True)



