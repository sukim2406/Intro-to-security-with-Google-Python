from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload')
def upload():
    return render_template('updown_upload.html')

@app.route('/upload_process', methods=['GET', 'POST'])
def upload_process():
    if request.method == 'POST':
        file_object = request.files['uploaded_file']
        file_object.save(secure_filename(file_object.filename))
        return 'File upload complete'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

