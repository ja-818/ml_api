import json
import time
from uuid import uuid4

import redis
import settings

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
  host = settings.REDIS_IP,
  port = settings.REDIS_PORT,
  db = settings.REDIS_DB_ID)


def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None

    # Assign an unique ID for this job and add it to the queue.
    job_id = str(uuid4())

    # Create a dict with the job data we will send through Redis having the
    job_data = {
      "id": job_id,
      "image_name": image_name,
    }

    # Send the job to the model service using Redis
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Loop until we received the response from our ML model
    while True:
        try:
          # Attempt to get model predictions using job_id
          output = json.loads(db.get(job_id))
          # Assign prediction to variables
          prediction = output["prediction"]
          score = output["score"]
          # Don't forget to delete the job from Redis after we get the results!
          db.delete(job_id)
          # Then exit the loop
          break
        except:
          pass        

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score
