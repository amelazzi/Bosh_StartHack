import httpauth as httpauth
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from constants import my_ip
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from create_messages import weather_message

auth = HTTPBasicAuth()

app = Flask(__name__)
api = Api(app)

last_message = {}

@app.route('/')
def index():
    return "Hello, World!"

@auth.get_password
def get_password(username):
    if username == 'bosch':
        return 'StartHack'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class Messages(Resource):
    def get(self):
        answer = {}
        weather = weather_message()
        if ('weather' not in last_message or last_message['weather'] != weather):
            answer['weather'] = weather
            last_message['weather'] = weather

        return answer


api.add_resource(Messages, '/messages')

if __name__ == '__main__':
    app.run(host = my_ip, port='5002')