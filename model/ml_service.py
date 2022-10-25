import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
  host=settings.REDIS_IP,
  port=settings.REDIS_PORT,
  db=settings.REDIS_DB_ID)

# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None
    
    # Load image
    img = image.load_img(f"./uploads/{image_name}", target_size=(224, 224))
    # Turn image into array
    x = image.img_to_array(img)
    # Add dimension for processing
    x_batch = np.expand_dims(x, axis=0)
    # Preprocess and prediction
    x_batch = preprocess_input(x_batch)
    preds = model.predict(x_batch)
    # Decode prediction
    raw_prediction = decode_predictions(preds, top=1)
    # Store prediction results
    class_name = raw_prediction[0][0][1]
    pred_probability = raw_prediction[0][0][2]

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        #   1. Take a new job from Redis
        queue_name, job_data = db.brpop(settings.REDIS_QUEUE)
        
        #   2. Run your ML model on the given data
        job_data = json.loads(job_data)
        model_prediction = predict(job_data["image_name"])
        
        #   3. Store model prediction in a dict with the following shape:
        prediction = {
          "prediction": model_prediction[0],
          "score": str(model_prediction[1])
        }
        
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        prediction = json.dumps(prediction)
        db.set(job_data["id"], prediction)

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
