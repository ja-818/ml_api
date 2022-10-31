import os
import settings
import utils
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
)
from middleware import model_predict

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # No file received, show basic UI
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        # File received but no filename is provided, show basic UI
        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)

        # File received and it's an image, we must show it and get predictions
        if file and utils.allowed_file(file.filename):
            #   1. Get an unique file name using utils.get_file_hash() function
            file_name = utils.get_file_hash(file)
            #   2. Store the image to disk using the new name
            file.save(os.path.join(settings.UPLOAD_FOLDER, file_name))
            
            #   3. Send the file to be processed by the `model` service
            raw_prediction = model_predict(file_name)
            
            #   4. Update `context` dict with the corresponding values
            context = {
                "prediction": raw_prediction[0],
                "score": raw_prediction[1],
                "filename": file_name,
            }

            return render_template("index.html", filename=file_name, context=context)
          
        # File received and but it isn't an image
        else:
            flash("Allowed image types are -> png, jpg, jpeg, gif")
            return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    rpse = {"success": False, "prediction": None, "score": None}
    #   1. Check a file was sent and that file is an image
    # No file received
    if "file" not in request.files:
        flash("No file part")
        return make_response(jsonify(rpse), 400)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return make_response(jsonify(rpse), 400)
    
    # File recieved and is of the proper type
    if file and utils.allowed_file(file.filename):
      #   2. Store the image to disk
      file_name = utils.get_file_hash(file)
      file.save(os.path.join(settings.UPLOAD_FOLDER, file_name))
      #   3. Send the file to be processed by the `model` service
      raw_prediction = model_predict(file_name)
      #   4. Update and return `rpse` dict with the corresponding values
      rpse = {"success": True, "prediction": raw_prediction[0], "score": float(raw_prediction[1])}
      return rpse
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    return make_response(jsonify(rpse), 400)


@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a plain text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    if request.method == "GET":
      return render_template("index.html")
    
    if request.method == "POST":
      if request.form.get("report") == None:
        return render_template("index.html")
      report = request.form.get("report")
      # Store the reported data to a file on the corresponding path
      with open(settings.FEEDBACK_FILEPATH, "a") as f:
        f.write(report + "\n")
      return render_template("index.html")