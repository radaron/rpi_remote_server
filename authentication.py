import bcrypt


def generate_salt():
    return bcrypt.gensalt()


def validate_password(password, record):
    return bcrypt.checkpw(password, record.password)


def hash_password(password, salt):
    return bcrypt.hashpw(password, salt)
