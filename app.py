import warnings
warnings.filterwarnings('ignore')

import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#####################################
# Flask Setup
#####################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Welcome to Hawaii Climate Analysis API!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start</br>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and percipitation"""
    # Query the dates and precipitation
    date_pcrps = session.query(Measurement.date, Measurement.prcp).all()

    # put into dictionary
    pcrp_list = []
    for result in date_pcrps:
        row = {'date':'pcrp'}
        row['date'] = result[0]
        row['pcrp'] = result[1]
        pcrp_list.append(row)
    return jsonify(pcrp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations from the table 
    all_stations = session.query(Station.station, Station.name).group_by(Station.station).all()

    station_list = list(np.ravel(all_stations))
    
    #jsonify
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temp observation for the previous year"""
    # Query the observations from the previous year
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        group_by(Measurement.date).\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').all()
    
    # put into list
    tobs_list = list(np.ravel(tobs_results))

    #jsonfy
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start=None):
    """Return a list of TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""
    # Query start date for TMIN, TAVG, TMAX
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    # put into list
    start_date_list = list(np.ravel(start_date))

    #jsonify
    return jsonify(start_date_list)

@app.route("/api/v1.0//<start>/<end>")
def start_end(start=None, end=None):
    """Return a list of TMIN, TAVG, TMAX for dates between the start and end date inclusive"""
    # Query start and end dates for TMIN, TAVG, TMAX
    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    
    # put into list
    start_end_date_list = list(np.ravel(start_end_date))

    #jsonfy
    return jsonify(start_end_date_list)
    
if __name__ == "__main__":
    app.run(debug=True)

    