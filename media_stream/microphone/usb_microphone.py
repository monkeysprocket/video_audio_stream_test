from typing import Generator
import pyaudio
from media_stream.microphone.base_microphone import BaseMicrophone

SAMPLE_RATE = 44100
BITS_PER_SAMPLE = 16
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK_SIZE = 4096


def _generate_wav_header() -> bytes:
    datasize = 2000 * 10 ** 6
    header = bytes("RIFF", "ascii")
    header += (datasize + 36).to_bytes(4, "little")
    header += bytes("WAVE", "ascii")
    header += bytes("fmt ", "ascii")
    header += (16).to_bytes(4, "little")
    header += (1).to_bytes(2, "little")
    header += (CHANNELS).to_bytes(2, "little")
    header += (SAMPLE_RATE).to_bytes(4, "little")
    header += (SAMPLE_RATE * CHANNELS * BITS_PER_SAMPLE // 8).to_bytes(4, "little")
    header += (CHANNELS * BITS_PER_SAMPLE // 8).to_bytes(2, "little")
    header += (BITS_PER_SAMPLE).to_bytes(2, "little")
    header += bytes("data", "ascii")
    header += (datasize).to_bytes(4, "little")
    return header


class USBMicrophone(BaseMicrophone):
    audio = pyaudio.PyAudio()

    def __init__(self):
        print("initialising USB microphone")
        super().__init__()

    @staticmethod
    def show_devices():
        count = USBMicrophone.audio.get_device_count()
        print(f"{count} devices found")
        for i in range(count):
            device = USBMicrophone.audio.get_device_info_by_index(i)
            if "USB" not in device.get("name"):
                continue
            print(device)

    @staticmethod
    def chunks() -> Generator[bytes, None, None]:
        stream = USBMicrophone.audio.open(
            rate=SAMPLE_RATE, channels=CHANNELS, format=FORMAT, input=True,
            input_device_index=1, frames_per_buffer=CHUNK_SIZE
        )
        yield _generate_wav_header() + stream.read(CHUNK_SIZE)
        while True:
            chunk = stream.read(CHUNK_SIZE)
            yield chunk


if __name__ == "__main__":
    mic = USBMicrophone()
    mic.chunks()
