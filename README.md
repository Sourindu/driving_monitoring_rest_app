# Driver's Time Monitoring Application

This is a python/flask based application running on docker container. This application provides framework for handling of the driver's "WORKING" and "DRIVING" clocks using in an in-memory redis (container) based cache.

The business logic for the application is as follows:

D + W + OFF (HOURS) = WORKING CLOCK
D = DRIVING CLOCK

Violation STATUS will be issued if:

DRIVING CLOCK > 11 HOURS -> Status V
WORKING CLOCK > 14 HOURS -> Status V

Clock Reset will be issued if:

Consecutive OFF Event sum is greater than 10 hours.
OFF(t,n-1) + OFF(t,n) > 10 -> Status OK,
DRIVING CLOCK = 0, WORKING CLOCK = 0.


## Installation/Run

The docker container is set up to be run on the go. Need to ensure docker daemon is running on the system.

```bash
cd <working_directory>
# For docker compose V2
docker compose up
# For docker compose V1
docker-compose -f docker-compose.yml
```

## Usage/Testing

```bash
# Posting data

curl --request POST 'localhost:5000/event' \
--header 'Content-Type: application/json' \
--data-raw '[
{
    "event": "D",
    "value": 1
},
{
    "event": "W",
    "value": 2
},
{
    "event": "OFF",
    "value": 3
}
]'

curl --request POST 'localhost:5000/event' \
--header 'Content-Type: application/json' \
--data-raw '[

{
    "event": "OFF",
    "value": 11
}
]'

curl --request POST 'localhost:5000/event' \
--header 'Content-Type: application/json' \
--data-raw '[

{
    "event": "D",
    "value": 1
},
{
    "event": "W",
    "value": 1
}
]'

# Fetching data

curl 'http://localhost:5000/event'
```

## Author
Sourindu Chatterjee