import hug
import falcon
import hug.development_runner
from multipart.hug_multipart import multipart

api = hug.API(__name__)
api.http.set_input_format("multipart/form-data", multipart)
route = hug.http(api=api)


@route.post("/upload")
def upload(**kwargs):
    file = kwargs.get("upload_file")
    if file:
        print(file.name)
    
    return file.name


if __name__ == "__main__":
    hug.development_runner.hug("app.py", port=9090)
