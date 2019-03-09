import httpauth as httpauth
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

from constants import my_ip
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from create_messages import weather_message
import os

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


PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


class Driver_mood(Resource):
    def get(self):
        return {"kek" : "lol"}
    def post(self):
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=True)



api.add_resource(Messages, '/messages')
api.add_resource(Driver_mood, '/driver_mood')

if __name__ == '__main__':

    app.run(host = my_ip, port='5002')