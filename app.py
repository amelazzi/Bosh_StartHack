from flask import Flask, request
from flask_restful import Resource, Api
from constants import my_ip

app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        return {'hello':'friend'}


api.add_resource(Hello, '/Hello')  # Route_1

if __name__ == '__main__':
    app.run(host = my_ip, port='5002')