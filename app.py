from flask import Flask, render_template, jsonify, request
import time
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# judge class of file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


# test_upload
@app.route('/')
def upload_test():
    return render_template('file_upload.html')


# upload_file
@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # get name in form
    if f and allowed_file(f.filename):  # judge class of file
        fname = f.filename
        print(fname)
        ext = fname.rsplit('.', 1)[1]  # get class of file
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # modify file name
        f.save(os.path.join(file_dir, new_filename))  # save file in dir
        token = new_filename
        print(token)
        return jsonify({"errno": 0, "errmsg": "success", "token": token})
    else:
        return jsonify({"errno": 1001, "errmsg": "fail"})


if __name__ == '__main__':
    app.run()
