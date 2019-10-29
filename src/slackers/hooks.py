import logging

from pyee import AsyncIOEventEmitter
from fastapi.encoders import jsonable_encoder


class NamedEventEmitter(AsyncIOEventEmitter):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        AsyncIOEventEmitter.__init__(self, *args, **kwargs)


events = NamedEventEmitter(name="events")
actions = NamedEventEmitter(name="actions")
commands = NamedEventEmitter(name="commands")


def emit(emitter, event, payload):
    jsonable = jsonable_encoder(payload)
    log = logging.getLogger(__name__)
    log.info(f"Emitting '{event}' using emitter '{emitter.name}'")
    log.debug(jsonable)

    emitter.emit(event, jsonable)