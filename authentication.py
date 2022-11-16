import bcrypt


def generate_salt():
    return bcrypt.gensalt()


def validate_password(password, record):
    return bcrypt.hashpw(password, record.salt) == record.password


def hash_password(password, salt):
    return bcrypt.hashpw(password, salt)