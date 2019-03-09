import httpauth as httpauth
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import json
from constants import my_ip,json_mis_path
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

class Mistakes(Resource):
    def get(self):
        # if (self.firsttime == 1):
        #     with open(json_mis_path, 'w') as json_file:
        #         json.dump([{}], json_file)
        #     self.firsttime = 0
        with open (json_mis_path) as json_file:
            data = json.load(json_file)[1:]
        with open(json_mis_path, 'w') as json_file:
            json.dump([{}], json_file)
        return data

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

from io import StringIO
import PIL.Image

from PIL import Image
from io import BytesIO
import re, time, base64

def getI420FromBase64(codec, image_path="c:\\"):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()
    img.save(image_path + str(t) + '.png', "PNG")


class Driver_mood(Resource):
    def get(self):
        return {"kek" : "lol"}
    def post(self):
        print(request.get_data()[6:])
        if ('image' in request.files):
            img = request.files['image']
            img_name = secure_filename(img.filename)
            create_new_folder(app.config['UPLOAD_FOLDER'])
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            # app.logger.info("saving {}".format(saved_path))
            img.save(saved_path)
            return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=True)
        else:
            img_name="photo.png"
            img = str(request.get_data()[6:len(request.get_data()) - 1])
            codec = 'data:image/png;base64,' + img
            getI420FromBase64(codec)
            return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=True)



api.add_resource(Messages, '/messages')
api.add_resource(Mistakes, '/mistakes')
api.add_resource(Driver_mood, '/driver_mood')

if __name__ == '__main__':
    app.run(host = my_ip, port='5002')