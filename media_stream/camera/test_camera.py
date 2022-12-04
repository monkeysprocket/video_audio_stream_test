from typing import Generator
import io
import numpy as np
from PIL import Image
from time import time, sleep

from media_stream.camera.base_camera import BaseCamera

HEIGHT = 128
WIDTH = 128


class TestCamera(BaseCamera):
    def __init__(self):
        print("initialising test camera")
        super().__init__()

    @staticmethod
    def frames() -> Generator[bytes, None, None]:
        print("starting test camera frames iterator")
        images = []
        for _ in range(3):
            image_array = np.random.rand(HEIGHT, WIDTH, 3) * 255
            image = Image.fromarray(image_array.astype('uint8')).convert("RGB")
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            byte_image = buffer.getvalue()
            images.append(byte_image)

        while True:
            print("yielding image")
            yield images[int(time()) % 3]
            sleep(1)
