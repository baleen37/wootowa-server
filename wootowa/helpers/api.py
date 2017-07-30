from typing import Dict

from flask import make_response, jsonify


def make_api_response(
        code: int = 200,
        msg: str = None,
        data: Dict[str, object] = None):
    if data:
        data = {}
    return make_response(jsonify({
        'code': code,
        'message': msg,
        'data': data
    })), code
