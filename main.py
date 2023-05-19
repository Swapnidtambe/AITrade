from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from app_property import AppProperty
import jwt
import datetime

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
        mobile_no = data['mobile_no']
        password = data['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s AND password = %s', (mobile_no, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            payload = {'mobile_no': mobile_no, 'password':password, 'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            response['data'] = [{'token': token}]
            response['errorCode'] = ''
            response['errorMessage'] = ''
            response['status'] = 'OK'
            # Redirect to home page
            return response
        else:
            # Account doesnt exist or username/password incorrect
            msg = app_property.get_message('101')
            response['data'] = ""
            response['errorCode'] = '101'
            response['errorMessage'] = msg
            response['status'] = 'FAIL'
            # Show the login form with message (if any)
        return response

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/ai_trade/logout', methods=['POST'])
def logout():
    response = {}
    data = request.get_json()
    token = data['token']
    blacklist.add(token)
    response['data'] = [{'message': 'Token has been logged out'}]
    response['errorCode'] = ''
    response['errorMessage'] = ''
    response['status'] = 'OK'
    return response

@app.route('/ai_trade/register', methods=['POST'])
def register():
    response = {}
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        data = request.get_json()
        # Create variables for easy access
        name = data['name']
        password = data['password']
        email = data['email']
        mobile = data['mobile']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile,))
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

        elif not re.match(r'^\d{10}$', mobile):
            response['data'] = ''
            response['errorMessage'] = app_property.get_message('104')
            response['errorCode'] = '104'
            response['status'] = 'FAIL'
            return response

        elif not mobile or not password or not email:
            response['data'] = ''
            response['errorMessage'] = app_property.get_message('105')
            response['errorCode'] = '105'
            response['status'] = 'FAIL'
            return response

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_accounts VALUES (NULL, %s, %s, %s,NULL,NULL, %s)', (name, password, email,mobile))
            mysql.connection.commit()
            response['data'] = [{'message': 'You have successfully registered!'}]
            response['errorMessage'] = ''
            response['errorCode'] = ''
            response['status'] = 'OK'
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
        mobile_no = payload['mobile_no']
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
        account = cursor.fetchone()
        response['data'] = [{'account':account}]
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
        mobile_no = payload['mobile_no']
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT end_date FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
        date = cursor.fetchone()
        end_date = date["end_date"]
        if end_date is None or end_date <= datetime.date.today():
            response['data'] = ""
            response['errorMessage'] = 'Subscription Expired'
            response['errorCode'] = '112'
            response['status'] = 'FAIL'
            return response
        else:
            cursor.execute('SELECT summary FROM summary WHERE currency = %s', ('GOLD',))
            summury = cursor.fetchone()
            response['data'] = [{"signal":'signal',"time":'time',"summury": summury}]
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
        response['data'] = [{'msg': msg}]
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

@app.route('/ai_trade/user/profile_update', methods=['POST'])
def profile_update():
    if request.method == 'POST':
        data = request.get_json()
        # Create variables for easy access
        name = data['name']
        old_pass = data['old_pass']
        new_pass = data['new_pass']
        email = data['email']

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
            mobile_no = payload['mobile_no']
            # We need all the account info for the user so we can display it on the profile page
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
            account = cursor.fetchone()
            password = account['password']
            if password == old_pass:
                try:
                    query = "UPDATE user_accounts SET "
                    fields = []
                    if name:
                        fields.append(f"name = '{name}'")
                    if new_pass:
                        fields.append(f"password = '{new_pass}'")
                    if email:
                        fields.append(f"email = '{email}'")

                    query += ", ".join(fields)
                    query += f" WHERE mobile_no = {mobile_no}"
                    # Execute the SQL query
                    cursor = mysql.connection.cursor()
                    cursor.execute(query)
                    mysql.connection.commit()

                    response['data'] = [{'message':"user profile updated"}]
                    response['errorMessage'] = ''
                    response['errorCode'] = ''
                    response['status'] = 'OK'
                    return response
                except:
                    response['data'] = ""
                    response['errorMessage'] = 'user profile not updated'
                    response['errorCode'] = '113'
                    response['status'] = 'FAIL'
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

@app.route('/ai_trade/admin/update', methods=['POST'])
def admin():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        # Create variables for easy access
        name = data['name']
        user_pass = data['password']
        old_mobile_no = data['old_mobile_no']
        mobile = data['mobile_no']
        email = data['email']
        start_date = data['start_date']
        end_date = data['end_date']

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
            mobile_no = payload['mobile_no']
            password = payload['password']
            # We need all the account info for the user so we can display it on the profile page
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s and password = %s', (mobile_no,password,))
            account = cursor.fetchone()
            mobile_no = account["mobile_no"]
            pas = account["password"]
            if mobile_no == '9527701111' and pas == 'Swappy969696':
                try:
                    query = "UPDATE user_accounts SET "
                    fields = []
                    if name:
                        fields.append(f"name = '{name}'")
                    if user_pass:
                        fields.append(f"password = '{user_pass}'")
                    if email:
                        fields.append(f"email = '{email}'")
                    if mobile:
                        fields.append(f"mobile_no = '{mobile}'")
                    if start_date:
                        fields.append(f"start_date = '{start_date}'")
                    if end_date:
                        fields.append(f"end_date = '{end_date}'")

                    query += ", ".join(fields)
                    query += f" WHERE mobile_no = {old_mobile_no}"

                    # Execute the SQL query
                    cursor = mysql.connection.cursor()
                    cursor.execute(query)
                    mysql.connection.commit()
                    response['data'] = [{'message':"user profile updated"}]
                    response['errorMessage'] = ''
                    response['errorCode'] = ''
                    response['status'] = 'OK'
                    return response
                except:
                    response['data'] = ""
                    response['errorMessage'] = 'user profile not updated'
                    response['errorCode'] = '113'
                    response['status'] = 'FAIL'
                    return response
            else:
                return "no admin"
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


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)



