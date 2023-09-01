import os
from pathlib import Path
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from PlantPredictorModel.plant_model import PlantDisease
import json
from dashApp.dash import getConfusionMatrixFigure

app = Flask(__name__)
dash_app = getConfusionMatrixFigure(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = os.path.join(BASE_DIR, "static\\image")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


model = PlantDisease()
model.load_model()


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
            filename = secure_filename(image.filename)  # type: ignore
            image_path = os.path.join(IMAGE_PATH, filename)
            image.save(image_path)
            values, classes = model.predict(image_path, 2)
            result = []
            file = open("treatment.json")
            data = json.load(file)
            treatment = {}

            if values[0] < 0.60:
                index = 0
                while (index < len(classes)):
                    result.append(
                        (classes[index], format(values[index] * 100, '.2f')))
                    treatment[classes[index]] = data[classes[index]]
                    index += 1

            else:
                result.append((classes[0], format(values[0] * 100, '.2f')))
                treatment[classes[0]] = data[classes[0]]
            return render_template("index.html",
                                   context={
                                       "imagePath": filename,
                                       "classes": classes,
                                       "result": result,
                                       "treatment": treatment
                                   })
    return render_template("index.html", context={"image": 1})


@app.route("/about", methods=["GET"])
def about():
    return dash_app.index()


if __name__ == "__main__":
    app.run(debug=True)
