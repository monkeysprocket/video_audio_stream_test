import threading
from time import time


class EventTimestamp:
    def __init__(self, event: threading.Event, timestamp: float):
        self.event = event
        self.timestamp = timestamp


class ChunkReadyEvent:
    def __init__(self):
        self.events: dict[int, EventTimestamp] = {}

    def wait(self):
        ident = threading.get_ident()
        if ident not in self.events:
            self.events[ident] = EventTimestamp(threading.Event(), time())
        return self.events[ident].event.wait()

    def set(self):
        now = time()
        remove = []
        for ident, event_timestamp in self.events.items():
            if not event_timestamp.event.is_set():
                event_timestamp.event.set()
                event_timestamp.timestamp = now
            else:
                if now - event_timestamp.timestamp > 5:
                    remove.append(ident)
        for item in remove:
            del self.events[item]

    def clear(self):
        self.events[threading.get_ident()].event.clear()

