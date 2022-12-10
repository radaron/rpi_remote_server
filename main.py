from flask import Flask, request, jsonify, render_template, session, redirect, abort
from database import init_db, get_session, RpiOrders, Authentication
from authentication import validate_password
from util import get_time, get_secret_key, validate_fields_exists

app = Flask(__name__, static_url_path="/rpi/static")
app.secret_key = get_secret_key()

init_db()

ORDER_KEYS = ("host", "port", "from_port", "to_port", "passwd", "username")
MANGE_KEYS = {"static": ("name", "host", "port", "from_port", "to_port", "passwd", "username"),
              "dynamic": ("name", "polled_time")
}


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")


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
        record.polled_time = get_time()
    else:
        record = RpiOrders(name=sender_name, polled_time=get_time())
        db_session.add(record)

    db_session.commit()
    db_session.close()
    return jsonify(resp)


@app.route("/rpi/manage/data", methods=['GET'])
def manage_data():
    if session.get("username"):
        db_session = get_session()

        resp = {}

        records = db_session.query(RpiOrders).all()

        for record in records:
            for data_type in MANGE_KEYS:
                if data_type not in resp:
                    resp[data_type] = []
                resp[data_type].append({k: getattr(record, k) for k in MANGE_KEYS[data_type]})

        db_session.close()
        return jsonify(resp)
    else:
        return abort(401)


@app.route("/rpi/manage", methods=['POST', 'GET'])
def manage():
    if session.get("username"):

        if request.method == "GET":
            db_session = get_session()

            records = db_session.query(RpiOrders).all()

            db_session.close()
            return render_template('manage.html')
        else:
            db_session = get_session()

            if name := request.form.get('connect'):
                if record := db_session.get(RpiOrders, name):
                    record.name = name
                    record.passwd = request.form.get(f'{name}_passwd')
                    record.host = request.form.get(f'{name}_host')
                    record.port = request.form.get(f'{name}_port')
                    record.from_port = request.form.get(f'{name}_from_port')
                    record.to_port = request.form.get(f'{name}_to_port')
                    record.username = request.form.get(f'{name}_username')
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
