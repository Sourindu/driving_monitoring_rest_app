from enum import Enum


class EventStatus(Enum):
    DRIVING = "D"
    WORKING = "W"
    OFFDUTY = "OFF"


class EventService:
    @staticmethod
    def set_default(cache):
        event_data = {}
        for event in EventStatus:
            event_data[event.value] = 0
        cache.set("event_data", event_data)

    @staticmethod
    def event_data(cache):
        return cache.get("event_data")

    @staticmethod
    def eval_driving_clock(event_data):
        status = {"violationStatus": "OK"}
        driving_curr_time = event_data[EventStatus.DRIVING.value]
        if driving_curr_time > 11:
            status["violationStatus"] = "V"
        status["hours"] = driving_curr_time
        return status

    @staticmethod
    def eval_working_clock(event_data):
        status = {"violation_status": "OK"}
        working_curr_time = event_data[EventStatus.WORKING.value]
        if working_curr_time > 14:
            status["violation_status"] = "V"
        status["hours"] = working_curr_time
        return status

    @staticmethod
    def store_event_data(cache, events):

        # Calculating input driving value
        in_driving_val = events[EventStatus.DRIVING.value]

        # Calculating input working value
        in_working_val = (
            events[EventStatus.WORKING.value]
            + events[EventStatus.DRIVING.value]
            + events[EventStatus.OFFDUTY.value]
        )

        # Calculaint input off-duty value
        in_off_val = events[EventStatus.OFFDUTY.value]

        # Fethcing data from the cache
        current_event_values = EventService.event_data(cache)

        # Parsing the data

        final_off_value = current_event_values[EventStatus.OFFDUTY.value] + in_off_val
        final_driving_value = (
            current_event_values[EventStatus.DRIVING.value] + in_driving_val
        )
        final_working_value = (
            current_event_values[EventStatus.WORKING.value] + in_working_val
        )

        # Applying Business logic
        # Resetting Driving and Working clock if total off val is greater than 10
        if final_off_value > 10:
            current_event_values[EventStatus.DRIVING.value] = 0
            current_event_values[EventStatus.WORKING.value] = 0
            current_event_values[EventStatus.OFFDUTY.value] = 0
        else:
            current_event_values[EventStatus.OFFDUTY.value] = final_off_value
            current_event_values[EventStatus.WORKING.value] = final_working_value
            current_event_values[EventStatus.DRIVING.value] = final_driving_value

        # Pushing the data to the cache
        cache.set("event_data", current_event_values)

    @staticmethod
    def get_clock_status(cache):
        response = []
        event_data = cache.get("event_data")
        response.append(
            {"type": "DRIVING_CLOCK", **EventService.eval_driving_clock(event_data)}
        )
        response.append(
            {"type": "WORKING_CLOCK", **EventService.eval_working_clock(event_data)}
        )
        return response
