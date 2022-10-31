from locust import HttpUser, task, between


class APIUser(HttpUser):
  wait_time = between(1, 5)

  @task(1)
  def index(self):
    self.client.get("http://0.0.0.0")
  
  @task(3)
  def predict(self):
    files = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jepg"))]
    headers = {}
    self.client.post("http://0.0.0.0/predict", headers=headers, files=files)