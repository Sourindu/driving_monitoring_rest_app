import pytest
from app.service import EventService


class MockRedisCache:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value


def test_set_default():
    cache = MockRedisCache()
    EventService.set_default(cache)
    data = {"event_data": {"D": 0, "W": 0, "OFF": 0}}
    assert cache.data == data


@pytest.mark.parametrize(
    "test_events,response",
    [
        [[{"event": "D", "value": 1}], {"event_data": {"D": 1, "W": 0, "OFF": 0}}],
        [
            [
                {"event": "D", "value": 1},
                {"event": "W", "value": 1},
                {"event": "D", "value": 1},
            ],
            {"event_data": {"D": 2, "W": 1, "OFF": 0}},
        ],
        [
            [
                {"event": "D", "value": 1},
                {"event": "W", "value": 1},
                {"event": "OFF", "value": 12},
            ],
            {"event_data": {"D": 1, "W": 1, "OFF": 12}},
        ],
    ],
)
def test_store_event_data(test_events, response):
    cache = MockRedisCache()
    EventService.set_default(cache)

    events = {"D": 0, "W": 0, "OFF": 0}

    for event in test_events:
        if event["event"] in events:
            events[event["event"]] = event["value"]

    EventService.store_event_data(cache, events)

    assert cache.data == response


@pytest.mark.parametrize(
    "test_events,response",
    [
        [
            [{"event": "D", "value": 1}],
            [
                {"type": "DRIVING_CLOCK", "violation_status": "OK", "hours": 1},
                {"type": "WORKING_CLOCK", "violation_status": "OK", "hours": 1},
            ],
        ],
        [
            [
                {"event": "D", "value": 1},
                {"event": "W", "value": 1},
                {"event": "D", "value": 1},
            ],
            [
                {"type": "DRIVING_CLOCK", "violation_status": "OK", "hours": 2},
                {"type": "WORKING_CLOCK", "violation_status": "OK", "hours": 3},
            ],
        ],
        [
            [
                {"event": "D", "value": 1},
                {"event": "W", "value": 1},
                {"event": "OFF", "value": 12},
            ],
            [
                {"type": "DRIVING_CLOCK", "violation_status": "OK", "hours": 0},
                {"type": "WORKING_CLOCK", "violation_status": "OK", "hours": 0},
            ],
        ],
        [
            [
                {"event": "D", "value": 10},
                {"event": "W", "value": 15},
                {"event": "OFF", "value": 2},
            ],
            [
                {"type": "DRIVING_CLOCK", "violation_status": "OK", "hours": 10},
                {"type": "WORKING_CLOCK", "violation_status": "V", "hours": 27},
            ],
        ],
    ],
)
def test_get_clock_status(test_events, response):
    cache = MockRedisCache()
    EventService.set_default(cache)

    events = {"D": 0, "W": 0, "OFF": 0}

    for event in test_events:
        if event["event"] in events:
            events[event["event"]] = event["value"]

    EventService.store_event_data(cache, events)

    res = EventService.get_clock_status(cache)
    assert res == response
