from flask import Blueprint, abort, request, jsonify, session
from rpi_remote_server.database import get_session, RpiOrder, RpiMetric
from rpi_remote_server.util import get_time
from rpi_remote_server.authentication import verify_username

METRIC_KEYS = ("uptime", "cpu_usage", "memory_usage", "disk_usage", "temperature")
MANGE_KEYS = ("name", "polled_time")

api = Blueprint('api', __name__)


@api.route("/api/metric", methods=['PUT'])
def put_metric():
    sender_name = request.json.get('name', None)

    db_session = get_session()
    order = db_session.get(RpiOrder, sender_name)

    if sender_name is None or order is None:
        db_session.close()
        return abort(401)

    metric = order.metric or RpiMetric()
    metric.name = sender_name

    for key in METRIC_KEYS:
        setattr(metric, key, request.json.get(key, None))
    order.metric = metric
    db_session.commit()
    db_session.close()

    return jsonify({"resp": "Ok"}), 200


@api.route("/api/order", methods=['GET'])
def get_order():
    sender_name = request.headers.get('name', None)
    username = request.headers.get('username', None)

    if sender_name is None:
        return abort(401)

    db_session = get_session()
    resp = {}

    if record := db_session.get(RpiOrder, sender_name):
        if record.port:
            resp = {"port": record.port}
        record.polled_time = get_time()
        record.username = username
    else:
        record = RpiOrder(name=sender_name, polled_time=get_time(), username=username)
        db_session.add(record)

    db_session.commit()
    db_session.close()
    return jsonify(resp)


@api.route("/api/data", methods=['GET'])
def manage_data():
    if verify_username(session.get('username')):
        db_session = get_session()
        resp = {"data": []}
        orders = db_session.query(RpiOrder).order_by(RpiOrder.name).all()

        for order in orders:
            resp['data'].append({k: getattr(order, k, "") for k in MANGE_KEYS})
            if order.metric:
                resp['data'][-1].update({k: getattr(order.metric, k, "") for k in METRIC_KEYS})

        db_session.close()
        resp["current_time"] = get_time()

        return jsonify(resp)
    return jsonify({"msg": "Unauthorized"}), 401


@api.route("/api/data", methods=['DELETE'])
def delete_data():
    if verify_username(session.get('username')):
        if data := request.json:
            db_session = get_session()

            if order_record := db_session.get(RpiOrder, data.get('name', '')):
                db_session.delete(order_record)
                db_session.commit()
                db_session.close()
            else:
                db_session.close()
                return "No Content", 204

            return jsonify({"resp": "Ok"}), 200

        return jsonify({"resp": "No content"}), 204
    return jsonify({"msg": "Unauthorized"}), 401
