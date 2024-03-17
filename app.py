from flask import Flask

UPLOAD_FOLDER = '/home/huy/Desktop/TL-tech/faceRA/facera_web_app/static/db_images/unknown'
REGISTER_FOLDER = '/home/huy/Desktop/TL-tech/faceRA/facera_web_app/static/db_images/unknown'


app = Flask(__name__)
app.secret_key = '1a2b3c4d5e'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['REGISTER_FOLDER'] = REGISTER_FOLDER