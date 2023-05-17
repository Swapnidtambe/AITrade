class AppProperty:
    def __init__(self):
        self.my_dict = {'101': 'Incorrect username/password!',
                        '102': 'Account already exists!',
                        '103': 'Invalid email address!',
                        '104': 'Username must contain only characters and numbers!',
                        '105': 'Please fill out the form!',
                        '106': 'You have not logged in',
                        '107': 'Authorization header is missing',
                        '108': 'Invalid token format',
                        '109': 'Token has been logged out',
                        '110': 'Token has expired',
                        '111': 'Invalid token',
                        '112': 'Subscription Expired',


                        }

    def print_dict(self):
        for key, value in self.my_dict.items():
            print(key, ':', value)

    def get_message(self,id):
        return self.my_dict.get(id)