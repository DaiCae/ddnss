from flask import request
from IPy import IP


def get_ip():
    # proxy ip
    raw_ip = request.headers.get("X-Real-IP")
    if raw_ip is None:
        # direct ip
        raw_ip = request.remote_addr
    # convert ipv4-mapped ipv6 to ipv4
    return raw_ip.replace("::ffff:", "")


def version(address):
    try:
        return IP(address).version()
    except Exception as e:
        return 0


def verify_v4(ip):
    try:
        address = IP(ip)
        if str(address) == str(ip) and address.version() == 4:
            return True
        else:
            return False
    except Exception as e:
        return False


def verify_v6(ip):
    try:
        address = IP(ip)
        if str(address) == str(ip) and address.version() == 6:
            return True
        else:
            return False
    except Exception as e:
        return False
