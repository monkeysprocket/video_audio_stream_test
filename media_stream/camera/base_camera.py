import threading
import time
from abc import ABC, abstractmethod
from typing import Generator

from .image_ready_event import ImageReadyEvent


class BaseCamera(ABC):
    thread = None
    frame = None
    last_access = 0
    image_event = ImageReadyEvent()

    def __init__(self):
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            BaseCamera.image_event.wait()

    @staticmethod
    def get_frame():
        BaseCamera.last_access = time.time()

        BaseCamera.image_event.wait()
        BaseCamera.image_event.clear()

        return BaseCamera.frame

    @staticmethod
    @abstractmethod
    def frames() -> Generator[bytes, None, None]:
        ...

    @classmethod
    def _thread(cls):
        print("starting camera thread")
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.image_event.set()
            time.sleep(0)

            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                break
        BaseCamera.thread = None
