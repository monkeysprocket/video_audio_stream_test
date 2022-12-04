from flask import render_template, Response
from media_stream import app
from media_stream.camera.camera_factory import camera_factory, CAMERA
from media_stream.microphone.microphone_factory import microphone_factory, MICROPHONE


@app.route("/")
def index():
    return render_template("index.html")


def image_gen(camera):
    yield b"--frame\r\n"
    while True:
        frame = camera.get_frame()
        yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n--frame\r\n"


def audio_gen(microphone):
    while True:
        chunk = microphone.get_chunk()
        yield chunk


@app.route("/video_feed")
def video_feed():
    return Response(
        image_gen(camera_factory(CAMERA.TEST)),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/audio_feed")
def audio_feed():
    return Response(
        audio_gen(microphone_factory(MICROPHONE.USB))
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
