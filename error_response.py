from app_property import AppProperty
app_property = AppProperty()
import logging
def Incorrect_username_password():
    response = {}
    # Account doesnt exist or username/password incorrect
    msg = app_property.get_message('101')
    response['data'] = ""
    response['errorCode'] = '101'
    response['errorMessage'] = msg
    response['status'] = 'FAIL'
    logging.info(f"Login response: {response}")
    return response

def Account_already_exists():
    response = {}
    response['data'] = ''
    response['errorMessage'] = app_property.get_message('102')
    response['errorCode'] = '102'
    response['status'] = 'FAIL'
    return response

def Invalid_email_address():
    response = {}
    response['data'] = ''
    response['errorMessage'] = app_property.get_message('103')
    response['errorCode'] = '103'
    response['status'] = 'FAIL'
    return response

def Mobile_number_is_not_valid():
    response = {}
    response['data'] = ''
    response['errorMessage'] = app_property.get_message('104')
    response['errorCode'] = '104'
    response['status'] = 'FAIL'
    return response

def Please_fill_out_the_form():
    response = {}
    response['data'] = ''
    response['errorMessage'] = app_property.get_message('105')
    response['errorCode'] = '105'
    response['status'] = 'FAIL'
    return response

def Authorization_header_is_missing():
    response = {}
    response["data"] = ''
    response['errorMessage'] = app_property.get_message('107')
    response['errorCode'] = '107'
    response['status'] = 'FAIL'
    return response

def Invalid_token_format():
    response = {}
    response["data"] = ''
    response['errorMessage'] = app_property.get_message('108')
    response['errorCode'] = '108'
    response['status'] = 'FAIL'
    return response

def Token_logged_out():
    response = {}
    response["data"] = ''
    response['errorMessage'] = app_property.get_message('109')
    response['errorCode'] = '109'
    response['status'] = 'FAIL'
    return response


def Token_has_expired():
    response = {}
    response["data"] = ''
    response['errorMessage'] = app_property.get_message('110')
    response['errorCode'] = '110'
    response['status'] = 'FAIL'
    return response

def Invalid_token():
    response = {}
    response['data'] = ''
    response['errorMessage'] = app_property.get_message('111')
    response['errorCode'] = '111'
    response['status'] = 'FAIL'
    return response

def Subscription_Expired():
    response = {}
    response['data'] = ""
    response['errorMessage'] = app_property.get_message('112')
    response['errorCode'] = '112'
    response['status'] = 'FAIL'
    return response

def User_profile_not_updated():
    response = {}
    response['data'] = ""
    response['errorMessage'] = app_property.get_message('113')
    response['errorCode'] = '113'
    response['status'] = 'FAIL'
    return response

def Token_not_received():
    response = {}
    response['data'] = ""
    response['errorMessage'] = app_property.get_message('114')
    response['errorCode'] = '114'
    response['status'] = 'FAIL'
    return response


def Password_not_correct():
    response = {}
    response['data'] = ""
    response['errorMessage'] = app_property.get_message('115')
    response['errorCode'] = '115'
    response['status'] = 'FAIL'
    return response

def user_profile_not_updated():
    response = {}
    response['data'] = ""
    response['errorMessage'] = app_property.get_message('116')
    response['errorCode'] = '116'
    response['status'] = 'FAIL'
    return response

def No_admin_authorization():
    response = {}
    response['data'] = ""
    response['errorMessage'] = app_property.get_message('117')
    response['errorCode'] = '117'
    response['status'] = 'FAIL'
    return response