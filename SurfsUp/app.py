# Import the dependencies.
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

from flask import Flask, jsonify, json
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################



app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    print("Welcome to our weather app")
    """List all available api routes."""
    return (
        f"Available routes:<br>" + 
        f"/api/v1.0/precipitation <br/>" +
        f"/api/v1.0/stations <br/>" +
        f"/api/v1.0/tobs <br/>" +
        f"/api/v1.0/start <br/>" +
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route('/api/v1.0/precipitation/')
@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    print("Precipitation")
    print(dir(recent_date))
    print(type(recent_date))

    last_year = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
   
   
      # Query the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        all()
        
        # Convert the results to a dictionary with 'date' as the key and 'prcp' as the value
    precipitation_dict = dict(results)
    return jsonify(precipitation_dict)



# Return a JSON-list of stations from the dataset.
@app.route('/api/v1.0/stations/')
def stations():
    print("In station section.")
    
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print("Station List:")
    all_stations = list(np.ravel(station_list))
    return jsonify(all_stations)



# Return a JSON-list of Temperature Observations from the dataset.
@app.route('/api/v1.0/tobs/')
@app.route('/api/v1.0/tobs')
def tobs():
    print("In TOBS section.")
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temp_obs = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= last_year)\
        .order_by(Measurement.tobs.desc()).all()
    print(f'{temp_obs}')

    D = {date: int(nobs) for date, nobs in list(temp_obs)}

    return jsonify(D)

    """
    D = {date: nobs for date, nobs in temp_obs}
    print(D)
    print("Out of TOBS section.")
    return jsonify(np.ravel(temp_obs))"
    """
# /api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start' page...")
    session = Session(engine)

    # Query for the min, avg, max temps for date >= start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    #session.close()

    # Convert list of tuples into normal list
    all_start_temps = list(np.ravel(results))

    return jsonify(all_start_temps)

# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    print("Server received request for 'Start-End' page...")
    session = Session(engine)

    # i like select() better than query(), but mehs
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    all_start_end_temps = list(np.ravel(results))

    return jsonify(all_start_end_temps)

if __name__ == "__main__":
    app.run(debug=True)
"""# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
@app.route('/api/v1.0/<start_date>/')
@app.route('/api/v1.0/<start_date>')
def calc_temps_start(start_date):
    print("In start date section.")
    print(start_date)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    all_start_temps = list(np.ravel(results))
    return jsonify(all_start_temps)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
@app.route('/api/v1.0/<start_date>/<end_date>/')
def calc_temps_start_end(start_date, end_date):
    print("In start & end date section.")
    print(Measurement.tobs)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    all_start_temps = list(np.ravel(results))
    return jsonify(all_start_temps)


if __name__ == "__main__":
    app.run(debug=True)
"""
