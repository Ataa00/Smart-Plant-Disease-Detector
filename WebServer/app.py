import os
from flask import Flask, request, render_template, redirect, flash, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/image'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # check if the post request has the file part
        if 'image' not in request.files:
            print('No file part')
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template("index.html", context={"image": filename})
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
