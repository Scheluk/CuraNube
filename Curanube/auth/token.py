from itsdangerous import URLSafeTimedSerializer
from flask import current_app

#generates a token that contains the email of the user
def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=str(current_app.config["SECURITY_PASSWORD_SALT"]))
    return serializer.dumps(email)

#validates a token
def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"],salt=str(current_app.config["SECURITY_PASSWORD_SALT"]))
    try:
        email = serializer.loads(
            token,
            max_age=expiration
        )
    except:
        return False
    return email