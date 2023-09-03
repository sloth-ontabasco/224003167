from re import M
import requests
import datetime

from flask_restful import Resource
import os

JOHN_DOE_BASE = os.getenv('JOHN_DOE_SERVER')
ACCESS_TOKEN = {
    'access_token': (None, None)
}


class CurrentTrainAPI(Resource):
    """
    Route: /api/trains
    """

    def get(self):
        access_token = ACCESS_TOKEN.get('access_token')
        print(access_token)
        if access_token[0] is None:
            res = requests.post(JOHN_DOE_BASE + '/train/auth', json={
                "companyname": os.getenv('companyname'),
                "clientID": os.getenv('clientID'),
                "clientSecret": os.getenv('clientSecret'),
                "ownerEmail": os.getenv('ownerEmail'),
                "ownerName": os.getenv('ownerName'),
                "rollNo": os.getenv('rollNo')
            })
            if res.status_code != 200:
                print('jehr', res.status_code)
                return {'error': 'John Doe server is down'}, 500
            ACCESS_TOKEN['token'] = res.json()['access_token']
            access_token = ACCESS_TOKEN.get('access_token')[0]

        elif access_token[1] < datetime.datetime.now().timestamp():
            res = requests.post(JOHN_DOE_BASE + '/train/auth', json={
                "companyname": os.getenv('companyname'),
                "clientID": os.getenv('clientID'),
                "clientSecret": os.getenv('clientSecret'),
                "ownerEmail": os.getenv('ownerEmail'),
                "ownerName": os.getenv('ownerName'),
                "rollNo": os.getenv('rollNo')
            })
            if res.status_code != 200:
                print(res.status_code)
                return {'error': 'John Doe server is down'}, 500
            ACCESS_TOKEN['token'] = res.json()['access_token']
            access_token = ACCESS_TOKEN.get('access_token')[0]

        res = requests.get(JOHN_DOE_BASE + '/train/trains', headers={
            "Authorization": "Bearer " + access_token[0]
        })

        if res.status_code != 200:
            return {'error': 'John Doe server is down'}, 500

        trains = res.json()

        now = datetime.datetime.now()
        filtered_trains = []
        for train in trains:
            train['departureTime'] = datetime.datetime(year=now.year,
                                                       month=now.month,
                                                       day=now.day,
                                                       hour=int(
                                                           train['departureTime']['Hours']),
                                                       minute=int(
                                                           train['departureTime']['Minutes']),
                                                       second=int(
                                                           train['departureTime']['Seconds']),
                                                       ) + datetime.timedelta(minutes=int(train['delayedBy']))
            if ((train['departureTime'] - now).seconds//60//60) <= 12:
                if ((train['departureTime'] - now).seconds//60//60) == 0 and ((train['departureTime'] - now).seconds//60) >= 30:
                    filtered_trains.append(train)

        # sort by price, then by seats available, then by departure time
        trains.sort(key=lambda x: (
            -x['departureTime'].timestamp(),
            -(x['seatsAvailable']['sleeper'] + x['seatsAvailable']['AC']),
            x['price']['sleeper']+x['price']['AC'],
        ))

        for train in trains:
            train['departureTime'] = train['departureTime'].strftime(
                '%Y-%m-%d %H:%M:%S')
        return {'trains':trains}, 200


class GetAccessToken(Resource):
    """
    Route: /api/auth
    """

    def get(self):
        res = requests.post(JOHN_DOE_BASE + '/train/auth', json={
            "companyName": os.getenv('companyName'),
            "clientID": os.getenv('clientID'),
            "clientSecret": os.getenv('clientSecret'),
            "ownerEmail": os.getenv('ownerEmail'),
            "ownerName": os.getenv('ownerName'),
            "rollNo": os.getenv('rollNo')
        })
        if res.status_code != 200:
            print(res.status_code)
            return {'error': 'John Doe server is down'}, 500
        ACCESS_TOKEN['access_token'] = (
            res.json()['access_token'], res.json()['expires_in'])
        return res.json(), 200
