from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {x.username: x for x in users}
userid_mapping = {x.id: x for x in users}


# Generates token on login
def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


# Takes in token for methods requiring authorization
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
