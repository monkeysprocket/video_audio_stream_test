from enum import Enum, auto

from media_stream.microphone.base_microphone import BaseMicrophone
from media_stream.microphone.usb_microphone import USBMicrophone


class MICROPHONE(Enum):
    USB = auto()


def microphone_factory(microphone: MICROPHONE) -> BaseMicrophone:
    if microphone is MICROPHONE.USB:
        return USBMicrophone()
    else:
        raise KeyError(f"{microphone} is not a valid option.")

