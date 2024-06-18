from datetime import datetime
from uuid import uuid4

class User:
    def __init__(self, login, secret):
        self.login = login
        self.secret = secret

class Method:
    def __init__(self, id, caption, json_params, description):
        self.id = id
        self.caption = caption
        self.json_params = json_params
        self.description = description

class Session:
    def __init__(self, user_id, method_id, data_in, data_out, status):
        self.id = str(uuid4())
        self.user_id = user_id
        self.method_id = method_id
        self.data_in = data_in
        self.data_out = data_out
        self.status = status
        self.created_at = datetime.now()
        self.time_op = 0  # Placeholder for operation time