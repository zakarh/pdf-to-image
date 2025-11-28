import os
import shutil
import tempfile
import traceback

from pathlib import Path

from flask import (
    Flask,
    abort,
    request,
    send_file,
)

from werkzeug.serving import WSGIRequestHandler
from werkzeug.utils import secure_filename

from doc import Doc
from helper import gen_id

doc = Doc()

app = Flask(__name__)
app.secret_key = gen_id(r=1)
WSGIRequestHandler.protocol_version = "HTTP/1.1"


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <title>upload</title>
            </head>
            <body>
                <form action="/api" method="post" enctype="multipart/form-data">
                    <p><input type="file" name="file">
                    <p><button type="submit">Submit</button>
                </form>
            </body>
            </html>"""


@app.route("/api", methods=["POST"])
def upload_file():
    """Upload a file and convert it into a GLTF and save it to Firebase."""
    if request.method == "POST":
        # Create a temporary directory.
        try:
            with tempfile.TemporaryDirectory(dir="") as directory:
                try:
                    # Reference file data.
                    document = request.files["file"]
                except Exception:
                    traceback.print_exc()
                    return abort(500)

                try:
                    # Create the 'data' directory to store converted files.
                    os.mkdir(os.path.join(os.getcwd(), directory, "data"))
                except Exception:
                    traceback.print_exc()
                    return abort(500)
                try:
                    # Secure document filename and save the document to the temporary directory.
                    filename = secure_filename(document.filename)
                    document.save(os.path.join(directory, filename))
                except Exception:
                    traceback.print_exc()
                    return abort(500)
                try:
                    # Convert the document page(s) into JPGs.
                    if doc.verify(filename):
                        if Path(filename).suffix in doc.supported_documents:
                            shutil.copyfile(
                                os.path.join(directory, filename),
                                os.path.join(directory, "data", filename),
                                follow_symlinks=False,
                            )
                        result = doc.convert(directory, filename)
                        if result:
                            # ZIP files in image directory and return as response.
                            name, extension = doc.extract(filename)
                            Path(directory).joinpath("data").joinpath(filename).unlink()
                            shutil.make_archive(
                                Path(directory).joinpath(filename),
                                "zip",
                                Path(directory).joinpath("data"),
                            )
                            return send_file(
                                Path(directory).joinpath(f"{filename}.zip"),
                                download_name=f"{name}.zip",
                                as_attachment=True,
                                mimetype="application/zip",
                            )
                        if not result:
                            return abort(500)
                except Exception:
                    traceback.print_exc()
                    return abort(500)
        except Exception:
            traceback.print_exc()
            return abort(500)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)
