from flask import Flask, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/")
def index():
    return redirect("/static/index.html")


@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)
    return "okay did something"


@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir("uploads/")
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)