from flask import request

from app.blueprints import Blueprint, new
from app.models import History, Record
from app.settings import config
from app.utils import client, cloudflare, response

bp = new(Blueprint("dns", __name__, url_prefix="/dns"))

DDNS_TOKEN = config.DDNS_TOKEN


@bp.before_request
def check_token():
    if DDNS_TOKEN is not None and request.values.get("token") != DDNS_TOKEN:
        return response.error("Auth failed!")


@bp.route("/")
def client_ip_info():
    return response.success("Get ip info success!", client.get_ip_info())


@bp.route("/update/<host>")
def update_record(host):
    ip_info = client.get_ip_info()
    ip_addr = ip_info.get("addr")
    ip_type = ip_info.get("type")

    record = Record.get_or_none(
        Record.host == host,
        Record.type == ip_type,
    )

    if record is None:
        record = Record(host=host, type=ip_type)
        record.name = cloudflare.get_record_name(record.host)
        record.id = cloudflare.get_record_id(record.name, record.type)
        if record.id is None:
            return response.error("Get record id failed!")

    # record no change
    if ip_addr == record.content:
        return response.success("The current record is already latest!", record)

    # set record content is new ip_addr
    record.content = ip_addr
    status = cloudflare.update_record(record.id, record.name, record.type, record.content)
    history = History(
        host=record.host,
        name=record.name,
        type=record.type,
        content=record.content,
        status=status,
    )
    record.save()
    history.save()

    if status:
        return response.success("Update record succeed!", record)
    else:
        return response.error("Update record failed!")
