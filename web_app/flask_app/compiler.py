import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
#from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import subprocess

from auth import login_required
from db import get_db

#bp = Blueprint('auth', __name__, url_prefix='/auth')
bp = Blueprint('compiler', __name__)
#bp = Blueprint('compiler', __name__, url_prefix='/compiler')

ALLOWED_EXTENSIONS = {'tex', 'png'}
UPLOAD_FOLDER = '/app/files/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT p.id, dir_path, name, num, tex, created, author_id, username"
        " FROM rireki p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    )
    posts = cursor.fetchall()
    cursor.close()
    #connection.close()
    return render_template('compiler/index.html', posts=posts)

def get_post(id, check_author=True):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT p.id, dir_path, name, num, tex, created, author_id, username"
        " FROM rireki p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = '{}'".format(id)
    )
    post = cursor.fetchone()
    cursor.close()
    #connection.close()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/result', methods=('GET', 'POST'))
@login_required
def result(id):
    post = get_post(id)
    return render_template('compiler/result.html', post=post)

@bp.route('/uploads/<num>/<name>')
def uploads(num, name):
    #UPLOAD_FOLDER = '/app/files/'
    dire = UPLOAD_FOLDER + num
    return send_from_directory(dire, name)

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
            #subprocess.run()
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # 拡張子を消したファイル名を取得する
            name = filename.rsplit('.', 1)[0]

            # 作業用ディレクトリを作成
            # 作業用ディレクトリにファイルをコピー
            # 作業用ディレクトリに移動
            # コンパイルの実施
            connection = get_db()
            cursor = connection.cursor(dictionary=True)
            #id_dir = int(cursor.lastrowid)
            cursor.execute("SELECT COUNT(*) FROM rireki WHERE author_id = {}".format(g.user['id']))
            count = cursor.fetchone()['COUNT(*)']
            dir_number = hash((g.user['id'], count)) + 2 ** 63
            dire = UPLOAD_FOLDER + str(dir_number) + "/"

            command = "mkdir -p {0} && cp {2}{1}.tex {0} && cd {0} && platex {1} && dvipdfmx {1}".format(dire, name, UPLOAD_FOLDER)
            subprocess.run(command, shell=True)
            #return redirect(url_for('compiler.uploaded_file', filename=filename))

            # 後の処理（ここは後で変えようと思う）
            compiled_name = name + ".pdf"
            #return redirect(url_for('compiler.compiled_file', compiled_name=compiled_name))

            cursor.execute(
                "INSERT INTO rireki (dir_path, tex, num, name, author_id)"
                " VALUES ('{}', '{}', '{}', '{}', {})".format(
                    dire, 'platex', str(dir_number), name, g.user['id']
                )
            )
            connection.commit()
            cursor.close()
            #connection.close()
            return redirect(url_for('compiler.index'))

    #return render_template('auth/register.html')
    return render_template('compiler/upload.html')
