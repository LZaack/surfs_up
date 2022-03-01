# Import dependencies datetime, NumPy, and Pandas
import datetime as dt
import numpy as np
import pandas as pd

# Import dependencies SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import denpendencies flask
from flask import Flask, jsonify

# Set up the database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into classes
Base = automap_base()

# Reflect the database
Base.prepare(engine, reflect=True)

# Create a variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to database
session = Session(engine)

# Define Flask app
app = Flask(__name__)

# Welcome route
@app.route("/")

# Create a function welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Route for precipitation analysis
@app.route("/api/v1.0/precipitation")

# Precipitation function
def precipitation():
    # Calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Create a dictionary with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in precipitation}
    # Jsonify the dictionary
    return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
