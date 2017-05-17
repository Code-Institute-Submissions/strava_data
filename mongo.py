from flask import Flask, render_template, request
from pymongo import MongoClient
import json

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'strava'
COLLECTION_NAME = 'stravanew'

app = Flask(__name__)

@app.route("/strava")
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
    with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to 55000
        projects = collection.find(projection=FIELDS, limit=55000)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(projects))

if __name__ == "__main__":
    app.run(debug=True)