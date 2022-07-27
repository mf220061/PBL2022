import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
#from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

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
            return redirect(url_for('compiler.uploaded_file', filename=filename))

    #return render_template('auth/register.html')
    return render_template('compiler/upload.html')
