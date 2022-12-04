import threading
import time
from abc import ABC, abstractmethod
from typing import Generator

from media_stream.microphone.chunk_ready_event import ChunkReadyEvent


class BaseMicrophone(ABC):
    thread = None
    chunk = None
    last_access = 0
    chunk_event = ChunkReadyEvent()

    def __init__(self):
        if BaseMicrophone.thread is None:
            BaseMicrophone.last_access = time.time()

            BaseMicrophone.thread = threading.Thread(target=self._thread)
            BaseMicrophone.thread.start()

            BaseMicrophone.chunk_event.wait()

    @staticmethod
    def get_chunk():
        BaseMicrophone.last_access = time.time()

        BaseMicrophone.chunk_event.wait()
        BaseMicrophone.chunk_event.clear()

        return BaseMicrophone.chunk

    @staticmethod
    @abstractmethod
    def chunks() -> Generator[bytes, None, None]:
        ...

    @classmethod
    def _thread(cls):
        print("starting microphone thread")
        chunk_iterator = cls.chunks()
        for chunk in chunk_iterator:
            BaseMicrophone.chunk = chunk
            BaseMicrophone.chunk_event.set()
            time.sleep(0)

            if time.time() - BaseMicrophone.last_access > 10:
                chunk_iterator.close()
                break
        BaseMicrophone.thread = None
