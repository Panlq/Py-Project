import hug
import falcon
import hug.development_runner
from middleware.multipart import MultipartMiddleware

api = hug.API(__name__)
api.http.add_middleware(MultipartMiddleware())
route = hug.http(api=api)


@route.post("/upload")
def upload(**kwargs):
    file = kwargs.get("upload_file")
    if file:
        print(file.name)
    
    return file.name


if __name__ == "__main__":
    hug.development_runner.hug("app2.py", port=9090)
