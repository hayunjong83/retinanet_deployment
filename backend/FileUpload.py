import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = './data_storage'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def fileUpload():
    target = os.path.join(UPLOAD_FOLDER, 'original_imgs')
    if not os.path.isdir(target):
        os.makedirs(target, exist_ok=True)

    logger.info("welcome to upload")

    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = os.path.join(target, filename)
    file.save(destination)
    session['uploadFilePath'] = destination
    response="whatever you wish too return"
    return response

if __name__ == '__main__':
    app.secret_key = os.urandom(42)
    app.run(debug=True, host="0.0.0.0",port=8000,use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')