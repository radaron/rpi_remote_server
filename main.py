from flask import Flask, request, jsonify, render_template, session, redirect, abort
from database import init_db, get_session, RpiOrders, Authentication
from authentication import validate_password
from util import get_time, get_secret_key, validate_fields_exists

app = Flask(__name__, static_url_path="/rpi/static")
app.secret_key = get_secret_key()

init_db()

ORDER_KEYS = ("host", "port", "from_port", "to_port", "passwd", "username")

@app.route("/rpi/order", methods=['GET'])
def get_order():
    sender_name = request.headers.get('name', None)

    if sender_name is None:
        return abort(401)

    db_session = get_session()
    resp = {}

    if record := db_session.get(RpiOrders, sender_name):
        if all([bool(getattr(record, value)) for value in ORDER_KEYS]):
            resp = {k: getattr(record, k) for k in ORDER_KEYS}
        record.polled_date = get_time()
    else:
        record = RpiOrders(name=sender_name, polled_date=get_time())
        db_session.add(record)

    db_session.commit()
    db_session.close()
    return jsonify(resp)


@app.route("/rpi/manage", methods=['POST', 'GET'])
def manage():
    if session.get("username"):

        if request.method == "GET":
            db_session = get_session()

            records = db_session.query(RpiOrders).all()

            db_session.close()
            return render_template('manage.html', records=records, current_date=get_time())
        else:
            db_session = get_session()

            if name := request.form.get('edit'):
                if record := db_session.get(RpiOrders, name):
                    record.name = name
                    record.passwd = request.form.get('passwd')
                    record.host = request.form.get('host')
                    record.port = request.form.get('port')
                    record.from_port = request.form.get('from_port')
                    record.to_port = request.form.get('to_port')
                    record.username = request.form.get('username')
            elif name := request.form.get('remove'):
                if record := db_session.get(RpiOrders, name):
                    db_session.delete(record)

            db_session.commit()
            db_session.close()
            return redirect("/rpi/manage")

    else:
        return redirect("/rpi/manage/login")


@app.route("/rpi/manage/login", methods=['POST', 'GET'])
def manage_login():
    if session.get("username"):
        return redirect("/rpi/manage")

    if request.method == 'GET':
        return render_template("login.html")

    if not validate_fields_exists(request.form, ["username", "password"]):
        return render_template("login.html", message="Invalid username or password!")

    db_session = get_session()

    if record := db_session.get(Authentication, request.form['username']):
        if validate_password(request.form["password"].encode(), record):
            session["username"] = request.form['username']

            db_session.close()
            return redirect("/rpi/manage")

    db_session.close()
    return render_template("login.html", message="Invalid username or password!")

@app.route("/rpi/manage/logout")
def manage_logout():
    session.pop("username", None)
    return redirect("/rpi/manage/login")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)
