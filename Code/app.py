import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """list all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("api/v1.0/precipitation")
def precipitation():
    one_y_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_y_ago).all()

    precipitation_df = pd.DataFrame(precipitation_data, columns=['date', 'precipitation'])
    precipitation_df = precipitation_df.sort_values("date")
    prcp_df_indexed = precipitation_df.set_index('date')

    prcp_dict = prcp_df_indexed.to_dict('dict')

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(Station.name, Station.station)
    stations_df = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
def tobs():
    one_y_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_y_ago).all()

    tobs_df = pd.DataFrame(tobs_data, columns=['date', 'tobs'])
    tobs_df = tobs_df.sort_values("date")
    tobs_df_indexed = precipitation_df.set_index('date')

    tobs_dict = tobs_df_indexed.to_dict('dict')

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    trip_start = dt.date(start_date) - dt.timedelta(days=365)
    end = dt.date(2017,8,23)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= trip_start).filter(Measurements.date <= end).all()

    trip_df = pd.DataFrame(trip_data, columns=['Min', 'avg', 'max'])
    trip_dict = trip_df.to_dict('dict')    
    return jsonify(trip_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    trip_start = dt.date(start_date) - dt.timedelta(days=365)
    trip_end =dt.date(end_date) - dt.timedelta(days=365)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= trip_start).filter(Measurements.date <= trip_end).all()

    trip_df = pd.DataFrame(trip_data, columns=['Min', 'avg', 'max'])
    trip_dict = trip_df.to_dict('dict')    
    return jsonify(trip_dict)


if __name__ == '__main__':
    app.run(debug=True)