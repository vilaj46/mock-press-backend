import jwt
from datetime import datetime, timedelta


class JWT:

    token = ""
    payload = {}

    secret = "secretsecret"
    algorithm = "HS256"

    def __init__(self, payload):
        one_day = timedelta(days=1)
        # one_day = timedelta(seconds=5)
        encoded_jwt = jwt.encode(
            {"exp": datetime.utcnow()+one_day, "payload": payload}, self.secret)

        # decoded_jwt = jwt.decode(
        #     encoded_jwt, self.secret, algorithms=["HS256"])

        self.token = encoded_jwt
        self.payload = payload

    def get(self):
        return str(self.token)

    def __str__(self):
        return self.token
