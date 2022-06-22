from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from config import Config

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=str(current_app.config["SECURITY_PASSWORD_SALT"]))
    return serializer.dumps(email)


def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except:
        return False
    return email