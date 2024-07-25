from flask import Flask, jsonify


class APIResponse:
    def __init__(self, status_code, message=None, data=None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def result(self):
        return jsonify({
            'status_code': self.status_code,
            'message': self.message,
            'data': self.data
        })