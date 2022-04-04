import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
from flask_caching import Cache
from app.service import EventService, EventStatus

config = dict(
    CACHE_TYPE=os.getenv("CACHE_TYPE"),  # redis
    CACHE_REDIS_HOST=os.getenv("CACHE_REDIS_HOST"),  # redis
    CACHE_REDIS_PORT=os.getenv("CACHE_REDIS_PORT"),  # 6379
    CACHE_REDIS_DB=os.getenv("CACHE_REDIS_DB"),  # 0
    CACHE_REDIS_URL=os.getenv("CACHE_REDIS_URL"),  # redis://redis:6379/0
    CACHE_DEFAULT_TIMEOUT=os.getenv("CACHE_DEFAULT_TIMEOUT"),  # 500
)

main_app = Flask(__name__)
main_app.config.update(config)
api = Api(main_app)
cache = Cache(main_app)

EventService.set_default(cache)


class HomeApi(Resource):
    def get(self):
        return jsonify({"status": "ok"})


class EventApi(Resource):
    def get(self):
        return jsonify({"status": "ok", "data": EventService.get_clock_status(cache)})

    def post(self):
        body = request.get_json()

        events = {"D": 0, "W": 0, "OFF": 0}

        # Flag to filter correct input data
        flag = 0
        for event in body:
            if event["event"] in events:
                events[event["event"]] = event["value"]
                flag = 1
        if flag:
            # Sending data to be parsed and stored
            EventService.store_event_data(cache, events)
            return jsonify({"status": "ok", "message": "saved"})
        else:
            return jsonify({"status": "not ok", "message": "bad input"})


def register_apis(application):
    api.add_resource(HomeApi, "/")
    api.add_resource(EventApi, "/event")
    return application


def setup(application):
    application = register_apis(application)
    return application
