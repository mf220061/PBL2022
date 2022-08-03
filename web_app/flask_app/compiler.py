import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
#from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import subprocess

from db import get_db

#bp = Blueprint('auth', __name__, url_prefix='/auth')
bp = Blueprint('compiler', __name__, url_prefix='/compiler')

ALLOWED_EXTENSIONS = {'tex', 'png'}
UPLOAD_FOLDER = '/app/files/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('/uploads/compiled/<compiled_name>')
def compiled_file(compiled_name):
    return send_from_directory(UPLOAD_FOLDER, compiled_name)

#@bp.route('/register', methods=('GET', 'POST'))
@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            name = filename.rsplit('.', 1)[0]
            command = "platex {} && dvipdfmx {}".format(name, name)
            subprocess.run(command, shell=True)
            #return redirect(url_for('compiler.uploaded_file', filename=filename))
            compiled_name = name + ".pdf"
            return redirect(url_for('compiler.compiled_file', compiled_name=compiled_name))

    #return render_template('auth/register.html')
    return render_template('compiler/upload.html')
