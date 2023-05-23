from flask import Flask
import datetime
import jwt
import logging
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)
from app_property import AppProperty
app_property = AppProperty()
import error_response
from main import blacklist
import re


def user_login(connection,data):
    logging.info(f"Received login request: {data}")
    response = {}
    mobile_no = data['mobile_no']
    password = data['password']
    cursor = connection.cursor(buffered=True)
    query = 'SELECT * FROM user_accounts WHERE mobile_no = %s AND password = %s'
    cursor.execute(query, (mobile_no, password))
    account = cursor.fetchone()
    if account:
        payload = {'mobile_no': mobile_no, 'password': password,
                   'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        response['data'] = [{'token': token}]
        response['errorCode'] = ''
        response['errorMessage'] = ''
        response['status'] = 'OK'
        # Logging the response
        logging.info(f"Login response: {response}")
        return response
    else:
        # Account doesnt exist or username/password incorrect
        response = error_response.Incorrect_username_password()
    return response

def user_logout(data):
    response = {}
    token = data['token']
    blacklist.add(token)
    response['data'] = [{'message': 'Token has been logged out'}]
    response['errorCode'] = ''
    response['errorMessage'] = ''
    response['status'] = 'OK'
    return response

def user_register(connection,data):
    response = {}
    logging.info(f"Received register request: {data}")
    # Create variables for easy access
    name = data['name']
    password = data['password']
    email = data['email']
    mobile = data['mobile']
    # Check if account exists using MySQL
    cursor = connection.cursor(buffered=True)
    cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile,))
    account = cursor.fetchone()
    # If account exists show error and validation checks
    if account:
        return error_response.Account_already_exists()

    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return error_response.Invalid_email_address()

    elif not re.match(r'^\d{10}$', mobile):
        return error_response.Mobile_number_is_not_valid()

    elif not mobile or not password or not email:
        return error_response.Please_fill_out_the_form()

    else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        query = ('INSERT INTO user_accounts VALUES (NULL, %s, %s, %s,NULL,NULL, %s)')
        data = (name, password, email, mobile)
        cursor.execute(query, data)
        connection.commit()
        response['data'] = [{'message': 'You have successfully registered!'}]
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response

def User_profile(connection,data):
    response = {}
    if not data:
        return error_response.Authorization_header_is_missing()
    parts = data.split()
    if parts[0].lower() != 'bearer':
        return error_response.Invalid_token_format()
    try:
        token = parts[1]
        if token in blacklist:
            return error_response.Token_logged_out()
    except:
        return error_response.Token_not_received()
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        mobile_no = payload['mobile_no']
        # We need all the account info for the user so we can display it on the profile page
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
        account = cursor.fetchone()
        response['data'] = [{'account':{"id":account[0],"name":account[1],"password":account[2],'email':account[3],
                                        "start_date":account[4],"end_date":account[5],"mobile_no":account[6] }}]
        response['errorMessage'] = ''
        response['errorCode'] = ''
        response['status'] = 'OK'
        return response
    except jwt.ExpiredSignatureError:
        return error_response.Token_has_expired()
    except jwt.InvalidTokenError:
        return error_response.Invalid_token()

def User_script_gold(connection,data):
    response = {}
    if not data:
        return error_response.Authorization_header_is_missing()
    parts = data.split()
    if parts[0].lower() != 'bearer':
        return error_response.Invalid_token_format()
    try:
        token = parts[1]
        if token in blacklist:
            return error_response.Token_logged_out()
    except:
        return error_response.Token_not_received()
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        mobile_no = payload['mobile_no']
        # We need all the account info for the user so we can display it on the profile page
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
        account = cursor.fetchone()
        end_date = account[5]
        if end_date is None or end_date <= datetime.date.today():
            return error_response.Subscription_Expired()
        else:
            cursor = connection.cursor(buffered=True)
            cursor.execute('SELECT summary FROM summary WHERE currency = %s', ('GOLD',))
            summury = cursor.fetchone()
            response['data'] = [{"signal":'signal',"time":'time',"summury": summury}]
            response['errorMessage'] = ''
            response['errorCode'] = ''
            response['status'] = 'OK'
            return response
    except jwt.ExpiredSignatureError:
        return error_response.Token_has_expired()
    except jwt.InvalidTokenError:
        return error_response.Invalid_token()

def User_script_euro(connection,data):
    response = {}
    if not data:
        return error_response.Authorization_header_is_missing()
    parts = data.split()
    if parts[0].lower() != 'bearer':
        return error_response.Invalid_token_format()
    try:
        token = parts[1]
        if token in blacklist:
            return error_response.Token_logged_out()
    except:
        return error_response.Token_not_received()
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        mobile_no = payload['mobile_no']
        # We need all the account info for the user so we can display it on the profile page
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
        account = cursor.fetchone()
        end_date = account[5]
        if end_date is None or end_date <= datetime.date.today():
            return error_response.Subscription_Expired()
        else:
            cursor.execute('SELECT summary FROM summary WHERE currency = %s', ('EURO',))
            summury = cursor.fetchone()
            response['data'] = [{"signal":'signal',"time":'time',"summury": summury}]
            response['errorMessage'] = ''
            response['errorCode'] = ''
            response['status'] = 'OK'
            return response
    except jwt.ExpiredSignatureError:
        return error_response.Token_has_expired()
    except jwt.InvalidTokenError:
        return error_response.Invalid_token()

def User_profile_update(connection,data,header):
    response = {}
    name = data['name']
    old_pass = data['old_pass']
    new_pass = data['new_pass']
    email = data['email']

    if not header:
        return error_response.Authorization_header_is_missing()
    parts = header.split()
    if parts[0].lower() != 'bearer':
        return error_response.Invalid_token_format()
    try:
        token = parts[1]
        if token in blacklist:
            return error_response.Token_logged_out()
    except:
        return error_response.Token_not_received()
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        mobile_no = payload['mobile_no']
        # We need all the account info for the user so we can display it on the profile page
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s', (mobile_no,))
        account = cursor.fetchone()
        password = account[2]
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
                cursor = connection.cursor(buffered=True)
                cursor.execute(query)
                connection.commit()

                response['data'] = [{'message': "user profile updated"}]
                response['errorMessage'] = ''
                response['errorCode'] = ''
                response['status'] = 'OK'
                return response
            except:
                return error_response.User_profile_not_updated()
        else:
            return error_response.Password_not_correct()
    except jwt.ExpiredSignatureError:
        return error_response.Token_has_expired()
    except jwt.InvalidTokenError:
        return error_response.Invalid_token()

def Admin_user_update(connection,data,header):
    response = {}
    name = data['name']
    user_pass = data['password']
    old_mobile_no = data['old_mobile_no']
    mobile = data['mobile_no']
    email = data['email']
    start_date = data['start_date']
    end_date = data['end_date']
    if not header:
        return error_response.Authorization_header_is_missing()
    parts = header.split()
    if parts[0].lower() != 'bearer':
        return error_response.Invalid_token_format()
    try:
        token = parts[1]
        if token in blacklist:
            return error_response.Token_logged_out()
    except:
        return error_response.Token_not_received()
    try:
        payload = jwt.decode(token, 'my_secret_key', algorithms='HS256')
        mobile_no = payload['mobile_no']
        password = payload['password']
        # We need all the account info for the user so we can display it on the profile page
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM user_accounts WHERE mobile_no = %s and password = %s', (mobile_no, password,))
        account = cursor.fetchone()
        mobile_no = account[6]
        pas = account[2]
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
                cursor = connection.cursor(buffered=True)
                cursor.execute(query)
                connection.commit()
                response['data'] = [{'message': "user profile updated"}]
                response['errorMessage'] = ''
                response['errorCode'] = ''
                response['status'] = 'OK'
                return response
            except:
                return error_response.User_profile_not_updated()
        else:
            return error_response.No_admin_authorization()
    except jwt.ExpiredSignatureError:
        return error_response.Token_has_expired()
    except jwt.InvalidTokenError:
        return error_response.Invalid_token()
