import os
import requests

from base64 import b64encode
from collections import defaultdict

from flask import Flask, request, redirect, flash, url_for, render_template
from werkzeug.utils import secure_filename

from config import *


# Config app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'something very secret'


def allowed_file(filename):
    """ Check file extention """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash(u"Can't read this file!", 'error')

        file = request.files['file']

        if file.filename == '':
            flash(u'File not choosen!', 'error')

        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                with open(f'images/{filename}', 'rb') as file:
                    img = file.read()
                data = defaultdict()
                data['img'] = b64encode(img).decode('utf-8')
                response = requests.post(
                    'http://192.168.68.22:8000/api/recognite_image',
                    json=dict(data)
                ).json()
                if 'error' in response.keys():
                    flash(response['error'], 'error')
                else:
                    flash(response['text'], 'discription')
                return redirect(url_for('upload_file', name=filename))
            else:
                flash(u"Not allowed extention of choosen file!", 'error')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
