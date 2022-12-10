import time

def get_time():
    return time.time()


def get_secret_key():
    return open("secret", 'r', encoding="utf-8").read()


def validate_fields_exists(request_form, values):
    return all([request_form.get(value, None) for value in values])