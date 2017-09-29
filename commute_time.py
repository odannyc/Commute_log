import begin
import requests
import arrow
from os import environ as env
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@begin.start
def run(
        time: 'The time you would like to check the directions in the format: YYYY-MM-DDTHH:mm:ss'
        =env.get('TIME', ''),
        key: 'Google maps API key that you are using.'=env.get('GOOGLE_MAPS_TOKEN', ''),
        timezone: 'The timezone for the time.'=env.get('TIMEZONE', 'US/Eastern'),
        origin: 'Origin address'=env.get('MAPS_ORIGIN', ''),
        destination: 'Destination Address'=env.get('MAPS_DESTINATION', ''),
        reverse: 'Whether to also print the Reverse route Directions'=env.get('REVERSE', False),
        verbose: 'Whether to print the output verbosely, or just use comma separated values.'=env.get('VERBOSE', False),
        ):

    if time and type(time) is str:
        # if no time, assume now. Time will be converted to timestamp since the
        # epoch
        departure_time = arrow.get(time, tz=timezone).timestamp
    else:
        departure_time = arrow.now().timestamp

    if not key:
        print("Need a google maps API key.\n")
        exit(1)

    params = dict()
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

    if verbose:
        print('From: {}'.format(origin))
        print('To: {}'.format(destination))
        print('Time: {}'.format(timestring))
        print('Duration: {}'.format(forwardtime))
        if reversetime:
            print('Reverse: {}'.format(reversetime))

    else:
        if reverse:
            print('{}, {}, {}'.format(timestring, forwardtime, reversetime))
        else:
            print('{}, {}'.format(timestring, forwardtime))
