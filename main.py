from flask import Flask, request
from sql_connection import get_sql_connection
app = Flask(__name__)
connection = get_sql_connection()
blacklist = set()
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
import user
import datetime
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)

@app.route('/ai_trade/login/', methods=['POST'])
def login():
    response = {}
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        data = request.get_json()
        return user.user_login(connection,data)

@app.route('/ai_trade/logout', methods=['POST'])
def logout():
    logging.info(f"Received logout request: {request.get_json()}")
    response = {}
    data = request.get_json()
    return user.user_logout(data)

@app.route('/ai_trade/register', methods=['POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        data = request.get_json()
        return user.user_register(connection, data)

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/ai_trade/profile', methods=['GET'])
def profile():
    data = request.headers.get('Authorization')
    return user.User_profile(connection,data)

@app.route('/ai_trade/script/gold')
def xauusd():
    data = request.headers.get('Authorization')
    return user.User_script_gold(connection,data)

@app.route('/ai_trade/script/euro')
def Euro():
    data = request.headers.get('Authorization')
    return user.User_script_euro(connection,data)

@app.route('/ai_trade/user/profile_update', methods=['POST'])
def profile_update():
    if request.method == 'POST':
        data = request.get_json()
        header = request.headers.get('Authorization')
        return user.User_profile_update(connection,data,header)

@app.route('/ai_trade/admin/update', methods=['POST'])
def admin():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        header = request.headers.get('Authorization')
        return user.Admin_user_update(connection,data,header)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)