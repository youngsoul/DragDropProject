from flask import Flask, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS, DATA

main_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Define an upload set of allowed extensions
data_files = UploadSet('data', TEXT+DOCUMENTS+DATA)

# define where the files will be updated to.  The name in UploadSet, data in this case,
# is part of the key name in the app.config. This is how it matches an upload directory
# with an UploadSet
app.config['UPLOADED_DATA_DEST'] = os.path.join(main_path, "uploads")

# configure the uploads extension
configure_uploads(app, data_files)


@app.route("/")
def index():
    return redirect("/static/index.html")


@app.route("/sendfile_orig", methods=["POST"])
def send_file_orig():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "./{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass

    return "successful_upload"

@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    saved_filename = data_files.save(fileob)

    return f"successful_upload: {saved_filename}"

@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir(app.config["UPLOAD_FOLDER"])

    #modify_time_sort = lambda f: os.stat("uploads/{}".format(f)).st_atime

    def modify_time_sort(file_name):
        file_path = "uploads/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=False)
