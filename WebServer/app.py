import os
from flask import Flask, request, render_template, redirect, flash, url_for
from werkzeug.utils import secure_filename
from PlantPredictorModel.plant_model import PlantDisease
import json
from dashApp.dash import getConfusionMatrixFigure

app = Flask(__name__)
getConfusionMatrixFigure(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/image'


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
        print(request.files)
        if image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)  # type: ignore
            image.save(os.path.join(UPLOAD_FOLDER, filename))

            image_path = os.path.abspath(filename).replace(
                "\\"+filename, url_for("static", filename="image/"+filename)).replace("\\", "/")
            values, classes = model.predict(image_path, 2)
            result = []
            file = open("treatment.json")
            data = json.load(file)
            treatment = {}

            if values[0] < 0.60:
                index = 0
                while (index < len(classes)):
                    result.append(
                        (classes[index], format(values[index], '.2f')))
                    treatment[classes[index]] = data[classes[index]]
                    index += 1

            else:
                result.append((classes[0], format(values[0], '.2f')))
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
    return render_template("about.html")
if __name__ == "__main__":
    app.run(debug=True)
