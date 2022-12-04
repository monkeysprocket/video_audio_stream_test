import io
from typing import Generator

import picamera
import time

from media_stream.camera.base_camera import BaseCamera


class PiCamera(BaseCamera):
    def __init__(self):
        print("initialising pi camera")
        super().__init__()

    @staticmethod
    def frames() -> Generator[bytes, None, None]:
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
