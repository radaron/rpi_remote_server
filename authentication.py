import bcrypt


def generate_salt():
    return bcrypt.gensalt()


def validate_password(password, record):
    return bcrypt.checkpw(password, bcrypt.hashpw(password, record.salt))


def hash_password(password, salt):
    return bcrypt.hashpw(password, salt)