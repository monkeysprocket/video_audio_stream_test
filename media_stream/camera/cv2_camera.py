from typing import Generator

import cv2
from media_stream.camera.base_camera import BaseCamera


class CV2Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        print("initialising cv2 camera")
        super().__init__()

    @staticmethod
    def frames() -> Generator[bytes, None, None]:
        camera = cv2.VideoCapture(CV2Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError("Unable to open camera")

        while True:
            _, img = camera.read()

            yield cv2.imencode(".jpg", img)[1].tobytes()

