# dependencies
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify, request

# db setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect db
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# save references
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# define Flask routes
@app.route("/")
def welcome():
    """list all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/2016-08-20'>2016-08-20</a><br/>"
        f"<a href='/api/v1.0/2016-08-20/2016-09-04'>2016-08-20/2016-09-04</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create sesssion
    session = Session(engine)

    # query
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # create dictionary
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # create session
    session = Session(engine)

    # query
    results = session.query(Station.station).all()

    session.close()

    # convert into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # create session
    session = Session(engine)

    # max/min dates
    max_date = session.query(func.max(Measurement.date)).first()
    max_date = pd.to_datetime(max_date)
    min_date = dt.date(max_date[0].year, max_date[0].month, max_date[0].day) - dt.timedelta(days=366)
    
    # get station activity
    stn_activity = session.query(Measurement.station, func.count(Measurement.station)\
        .label('qty'))\
        .group_by(Measurement.station)\
        .order_by(desc('qty'))\
        .all()

    top_stn = stn_activity[0][0]

    # query
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
        .filter(Measurement.date > min_date)\
        .filter(Measurement.station == top_stn)\
        .order_by(Measurement.date)\
        .all()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def user_temps_start(start):
    # create session
    session = Session(engine)

    # query
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)\
        .all()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def user_temps_start_end(start, end):
    # create session
    session = Session(engine)

    # query
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)\
        .all()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)