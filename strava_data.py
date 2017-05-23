from stravalib.client import Client, unithelper
from flask import Flask, render_template, request
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DBS_NAME = os.getenv('MONGO_DB_NAME', 'strava')

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
COLLECTION_NAME = 'stravanew'


def get_key():
    GET_CODE = request.args.get('code')

    # def get_code(data):
    #     file_name = raw_input('Enter file name')
    #     with open("C:/" + file_name + '.txt', 'a') as text_file:
    #         text_file.write(data + '\n')

    AUTH_CODE = GET_CODE
    MY_STRAVA_CLIENT_ID = 17090
    MY_STRAVA_CLIENT_SECRET = '0f9539d9badcf88fd4a5853a0173f709569c9f6d'

    client = Client()

    JAMES_TOKEN = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,
                                                 client_secret=MY_STRAVA_CLIENT_SECRET,
                                                 code=AUTH_CODE)

    client = Client(access_token=JAMES_TOKEN)
    athlete = client.get_athlete()

    # def ath_data():
    #     data = {'firstname': athlete.firstname, 'lasttname': athlete.lastname, 'id': athlete.id, 'city': athlete.city, 'friends': athlete.friend_count}
    #     datafied = str(data)
    #     json_data = json.dumps(datafied)
    #     print json_data

    def activity_get():
        for activity in client.get_activities(after='2012', limit=0):
            miles = int(unithelper.miles(activity.distance))
            time = str(activity.moving_time)
            start_date = str(activity.start_date)
            year_month = start_date[:10]
            elevation = int(unithelper.feet(activity.total_elevation_gain))
            avg = int(unithelper.miles_per_hour(activity.average_speed))
            max = int(unithelper.miles_per_hour(activity.max_speed))
            data = {'Start Date': year_month, 'RideName': activity.name, 'Distance': miles, 'Time': time,
                    'Elevation': elevation, 'AthleteName': athlete.firstname + ' ' + athlete.lastname,
                    'StravaID': athlete.id, 'AverageSpeed': avg, 'MaxSpeed': max, 'Kudos': activity.kudos_count,
                    'jamesavg': avg}
            # data = {'johnavg':avg, 'StartDate':year_month}
            json_str = json.dumps(data)
            with open("C:/test.json", "a") as f:
                f.write(json_str + "\n")
    activity_get()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route("/data")
def strava_data():
    """
        A Flask view to serve the project data from
        MongoDB in JSON format.
        """

    # A constant that defines the record fields that we wish to retrieve.
    FIELDS = {
        '_id': False, 'Strava ID': True, 'Elevation (Ft)': True,
        'Kudos': True, 'Average Speed(Mph)': True,
        'Max Speed': True, 'Ride Name': True, 'Time': True,
        'Start Date': True, 'Distance(Mi)': True, 'Athlete Name': True
    }

    # Open a connection to MongoDB using a with statement such that the
    # connection will be closed as soon as we exit the with statement
    with MongoClient(MONGO_URI) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to 55000
        projects = collection.find(projection=FIELDS, limit=55000)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(projects))

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/authgood')
def exchange():
    get_key()
    return render_template('token_exchange.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run()

