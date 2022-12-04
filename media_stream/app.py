from flask import render_template, Response
from media_stream import app
from media_stream.camera.camera_factory import camera_factory, CAMERA


@app.route("/")
def index():
    return render_template("index.html")


def gen(camera):
    yield b"--frame\r\n"
    while True:
        frame = camera.get_frame()
        print(frame)
        yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n--frame\r\n"


@app.route("/video_feed")
def video_feed():
    return Response(
        gen(camera_factory(CAMERA.TEST)),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
