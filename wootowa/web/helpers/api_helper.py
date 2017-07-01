from typing import Dict

from flask import make_response, jsonify


class APIHelper(object):
    @classmethod
    def make_api_response(cls, code: int = 200, message=str, data=Dict[str, object]):
        return make_response(jsonify({
            'code': code,
            'message': message,
            'data': data
        })), code
