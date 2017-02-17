import begin

import requests

import arrow


@begin.start
def run(
        time: 'The time you would like to check the directions in the format: YYYY-MM-DDTHH:mm:ss'='',
        key: 'Google maps API key that you are using.'='',
        timezone: 'The timezone for the time.'='US/Eastern',
        origin: 'Origin address'='1 Madison Ave, New York, NY',
        destination: 'Destination Address'='1 Central Park South, New York, NY',
        reverse: 'Whether to also print the Reverse route Directions'=False,
        verbose: 'Whether to print the output verbosely, or just use comma separated values.'=False,
        ):
    if not time:
        # if no time, assume now. Time will be converted to timestamp since the
        # epoch
        departure_time = arrow.now().timestamp
    else:
        departure_time = arrow.get(time, tz=timezone).timestamp

    if not key:
        print("Need a google maps API key.\n")
        return

    params = {}
    params['origin'] = origin
    params['destination'] = destination
    params['key'] = key
    params['departure_time'] = departure_time

    r = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params=params
    )
    forwardtime = ''
    reversetime = ''
    routes = r.json()['routes']
    for route in routes:
        for leg in route['legs']:
            forwardtime = leg['duration_in_traffic']['text']

    if reverse:
        params['origin'] = destination
        params['destination'] = origin

        r = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params=params
        )

        routes = r.json()['routes']
        for route in routes:
            for leg in route['legs']:
                reversetime = leg['duration_in_traffic']['text']

    timestring = arrow.now().format()

    if(verbose):
        print("Time = {}".format(timestring))
        print('Duration:')
        print(forwardtime)
        if(reversetime):
            print("Reverse:")
            print(reversetime)

    else:
        if(reverse):
            print('{}, {}, {}'.format(timestring, forwardtime, reversetime))
        else:
            print('{}, {}'.format(timestring, forwardtime))
