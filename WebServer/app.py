from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])

def index():
    context = {
        "name": "Name",
        "age": 23 
    }
    return render_template("index.html", context=context)
    
if __name__ == "__main__":
    app.run(debug=True)