import bcrypt
from rpi_remote_server.database import get_session, Authentication

def generate_salt():
    return bcrypt.gensalt()


def validate_password(password, record):
    return bcrypt.checkpw(password, record.password)


def hash_password(password, salt):
    return bcrypt.hashpw(password, salt)


def verify_username(username):
    db_session = get_session()
    return_value = bool(db_session.get(Authentication, username))
    db_session.close()
    return return_value
