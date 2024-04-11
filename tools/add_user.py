import sys
import getpass
from rpi_remote_server.database import init_db, get_session, Authentication
from rpi_remote_server.authentication import generate_salt, hash_password


def main():
    init_db()

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    if not username or not password:
        sys.exit(1)

    salt = generate_salt()
    password = hash_password(password.encode(), salt)

    db_session = get_session()

    if record := db_session.get(Authentication, username):
        record.password = password
        record.salt = salt
    else:
        record = Authentication(username=username,
                                password=password,
                                salt=salt)
        db_session.add(record)

    db_session.commit()

    db_session.close()


if __name__ == "__main__":
    main()
