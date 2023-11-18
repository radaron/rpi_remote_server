from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import jwt_required
from rpi_remote_server.database import get_session, RpiOrders 
from rpi_remote_server.util import get_time 

ORDER_KEYS = ("host", "port", "from_port", "to_port", "passwd", "username")
MANGE_KEYS = ("name", "polled_time")

api = Blueprint('api', __name__)


@api.route("/rpi/order", methods=['GET'])
@api.route("/rpi/api/order", methods=['GET'])
def get_order():
    sender_name = request.headers.get('name', None)

    if sender_name is None:
        return abort(401)

    db_session = get_session()
    resp = {}

    if record := db_session.get(RpiOrders, sender_name):
        if all(bool(getattr(record, value)) for value in ORDER_KEYS):
            resp = {k: getattr(record, k) for k in ORDER_KEYS}
        record.polled_time = get_time()
    else:
        record = RpiOrders(name=sender_name, polled_time=get_time())
        db_session.add(record)

    db_session.commit()
    db_session.close()
    return jsonify(resp)


@api.route("/rpi/api/data", methods=['GET'])
@jwt_required()
def manage_data():
    db_session = get_session()
    resp = {"data" : []}
    records = db_session.query(RpiOrders).all()

    for record in records:
        resp['data'].append({k: getattr(record, k) if getattr(record, k)
                                else "" for k in MANGE_KEYS})

    db_session.close()
    resp["current_time"] = get_time()

    return jsonify(resp)


@api.route("/rpi/api/data", methods=['DELETE'])
@jwt_required()
def delete_data():
    if data := request.json:
        db_session = get_session()

        if record := db_session.get(RpiOrders, data.get('name', '')):
            db_session.delete(record)
            db_session.commit()
            db_session.close()
        else:
            db_session.close()
            return "No Content", 204

        return jsonify({"resp": "Ok"}), 200

    return jsonify({"resp": "No content"}), 204