from enum import Enum, auto

from media_stream.camera.base_camera import BaseCamera
# from media_stream.camera.pi_camera import PiCamera
from media_stream.camera.test_camera import TestCamera


class CAMERA(Enum):
    TEST = auto()
    PI = auto()


def camera_factory(camera: CAMERA) -> BaseCamera:
    if camera is CAMERA.TEST:
        return TestCamera()
    # elif camera is CAMERA.PI:
    #     return PiCamera()
    else:
        raise KeyError(f"{camera} is not a valid option.")
